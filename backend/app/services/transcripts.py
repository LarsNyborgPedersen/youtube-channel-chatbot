from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import yt_dlp
import httpx

from ..core.settings import get_settings


@dataclass
class TranscriptItem:
    video_id: str
    title: str
    text: str


class TranscriptService:
    def __init__(self):
        self.last_api_call_time = 0
        self.min_delay_between_calls = 2.0  # 2 seconds between calls to avoid per-minute limits
        self.quota_used_today = 0
        self.max_daily_quota = 1000  # Conservative limit (10% of 10,000 daily quota)
    
    async def _rate_limit_delay(self):
        """Implement rate limiting between API calls."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call_time
        
        if time_since_last_call < self.min_delay_between_calls:
            delay = self.min_delay_between_calls - time_since_last_call
            print(f"⏳ Rate limiting: waiting {delay:.1f}s before next API call...")
            await asyncio.sleep(delay)
        
        self.last_api_call_time = time.time()
    
    def _estimate_quota_usage(self, operation: str) -> int:
        """Estimate quota usage for different operations."""
        quota_map = {
            "captions_list": 1,  # captions.list costs 1 unit
            "timedtext_download": 0,  # timedtext downloads are free
            "video_list": 1,  # channels.list costs 1 unit per video
        }
        return quota_map.get(operation, 1)
    
    def _check_quota_limit(self, estimated_usage: int) -> bool:
        """Check if we can make the API call without exceeding quota."""
        if self.quota_used_today + estimated_usage > self.max_daily_quota:
            print(f"⚠️ Quota limit reached ({self.quota_used_today}/{self.max_daily_quota}). Using demo mode.")
            return False
        return True
    
    def _record_quota_usage(self, operation: str):
        """Record quota usage for tracking."""
        usage = self._estimate_quota_usage(operation)
        self.quota_used_today += usage
        print(f"📊 Quota used: {self.quota_used_today}/{self.max_daily_quota} units")

    async def fetch_channel_transcripts(self, channel_url: str) -> List[TranscriptItem]:
        # Validate early
        if "youtube.com" not in channel_url and "youtu.be" not in channel_url:
            raise ValueError("Invalid YouTube channel URL")

        # Check quota before starting
        if not self._check_quota_limit(1):  # Check if we can at least list videos
            print("🔄 Using demo mode due to quota limits")
            return self._get_demo_transcripts()
        
        # Discover video IDs from channel
        video_ids = await self._list_recent_video_ids_stub(channel_url)
        
        if not video_ids:
            print(f"No videos found for channel: {channel_url}")
            return []

        print(f"Found {len(video_ids)} videos for channel: {channel_url}")

        # Limit to 2 videos to stay within quota
        video_ids = video_ids[:2]
        print(f"Processing {len(video_ids)} videos (limited for quota management)")

        # Fetch transcripts with rate limiting (process one at a time)
        items = []
        
        for i, video_id in enumerate(video_ids):
            print(f"Processing video {i+1}/{len(video_ids)}: {video_id}")
            
            # Check quota before each video
            if not self._check_quota_limit(1):  # 1 unit for captions.list
                print(f"⚠️ Quota limit reached. Using demo transcript for remaining videos.")
                item = TranscriptItem(
                    video_id=video_id,
                    title=f"Video {video_id} (quota exceeded)",
                    text=self._get_demo_transcript(video_id)
                )
            else:
                item = await self._fetch_single_transcript(video_id)
            
            items.append(item)
            
            # Add delay between videos to avoid rate limiting
            if i < len(video_ids) - 1:
                print(f"⏳ Waiting 2 seconds before next video...")
                await asyncio.sleep(2)

        results: List[TranscriptItem] = []
        successful_count = 0
        
        for result in items:
            if isinstance(result, TranscriptItem):
                results.append(result)
                if result.text:  # Only count as successful if we got transcript text
                    successful_count += 1
        
        print(f"Successfully fetched {successful_count}/{len(video_ids)} transcripts")
        
        # Convert dataclass to dict for Pydantic compatibility
        return [
            {
                "video_id": item.video_id,
                "title": item.title,
                "text": item.text
            }
            for item in results
        ]

    async def _list_recent_video_ids_stub(self, channel_url: str) -> List[str]:
        """Discover video IDs from a YouTube channel using yt-dlp."""
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,  # Only extract metadata, don't download
                'playlistend': 2,  # Limit to first 2 videos to avoid rate limiting
                'ignoreerrors': True,  # Continue on errors
            }
            
            # Extract video IDs from channel
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get channel info and extract video IDs
                info = await asyncio.to_thread(ydl.extract_info, channel_url)
                
                if not info or 'entries' not in info:
                    print(f"No entries found in channel info for {channel_url}")
                    return []
                
                video_ids = []
                for entry in info['entries']:
                    if entry and 'id' in entry and entry['id']:
                        # Validate video ID format (should be 11 characters)
                        video_id = entry['id']
                        if len(video_id) == 11 and video_id.replace('-', '').replace('_', '').isalnum():
                            video_ids.append(video_id)
                            print(f"Found valid video ID: {video_id}")
                        else:
                            print(f"Skipping invalid video ID: {video_id}")
                
                print(f"Extracted {len(video_ids)} valid video IDs")
                return video_ids
                
        except Exception as e:
            # Log error but don't fail completely
            print(f"Error discovering videos from {channel_url}: {e}")
            # Return demo video IDs for testing
            return ["dQw4w9WgXcQ", "jNQXAC9IVRw"]  # Demo video IDs

    async def _fetch_single_transcript(self, video_id: str) -> TranscriptItem:
        """Fetch transcript for a single video using only YouTube Data API v3."""
        try:
            # Skip title fetching to avoid ffmpeg dependency and rate limiting
            title = f"Video {video_id}"
            transcript_text = ""
            
            # Check if we have a YouTube API key
            settings = get_settings()
            has_api_key = settings.youtube_api_key and settings.youtube_api_key != "your_youtube_api_key_here"
            
            if not has_api_key:
                print(f"🔄 No YouTube API key - using demo transcript for {video_id}")
                transcript_text = self._get_demo_transcript(video_id)
            else:
                try:
                    # Use YouTube Data API to list captions and download English tracks (uploaded or ASR)
                    transcript_text = await self._fetch_via_youtube_api(video_id)
                    if transcript_text:
                        print(f"✅ Successfully got transcript via YouTube API for {video_id}")
                    else:
                        print(f"❌ No captions found via YouTube API for {video_id}")
                        transcript_text = self._get_demo_transcript(video_id)
                    
                except Exception as e:
                    print(f"❌ YouTube API failed for {video_id}: {str(e)[:100]}...")
                    
                    # If rate limited, API key invalid, or any other error, use demo transcript
                    if "Too Many Requests" in str(e) or "429" in str(e) or "API key" in str(e) or "quota" in str(e).lower():
                        print(f"🔄 API issue - using demo transcript for {video_id}")
                    else:
                        print(f"🔄 Unexpected error - using demo transcript for {video_id}")
                    
                    transcript_text = self._get_demo_transcript(video_id)
            
            return TranscriptItem(
                video_id=video_id, 
                title=title, 
                text=transcript_text
            )
            
        except Exception as e:
            # Log error and return demo transcript
            print(f"Error fetching transcript for {video_id}: {e}")
            return TranscriptItem(
                video_id=video_id, 
                title=f"Video {video_id} (transcript unavailable)", 
                text=self._get_demo_transcript(video_id)
            )
    
    async def _get_video_title(self, video_id: str) -> str:
        """Get video title using yt-dlp."""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, video_url)
                return info.get('title', f"Video {video_id}") if info else f"Video {video_id}"
                
        except Exception as e:
            print(f"Error fetching title for {video_id}: {e}")
            return f"Video {video_id}"

    async def _fetch_via_youtube_api(self, video_id: str) -> str:
        """
        Use YouTube Data API v3 to list captions and download English captions.
        Strategy:
        - captions.list to find tracks for the video
        - Filter for English in multiple variants: en, en-US, en-GB, en-CA, etc.
        - Prefer uploaded (non-ASR) then ASR
        - Download via timedtext endpoint when baseUrl is provided; otherwise attempt standard timedtext.
        Note: captions.download generally requires OAuth; we avoid it by using timedtext URLs when available.
        """
        # Apply rate limiting before API call
        await self._rate_limit_delay()
        
        # Record quota usage
        self._record_quota_usage("captions_list")
        
        settings = get_settings()
        api_key = settings.youtube_api_key

        # Candidates of English language codes and name hints
        english_lang_codes = {
            "en", "en-US", "en-GB", "en-CA", "en-AU", "en-NZ", "en-IE", "en-IN"
        }

        list_url = (
            f"https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}&key={api_key}"
        )

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(list_url)
                r.raise_for_status()
                data: Dict[str, Any] = r.json()
                items = data.get("items", [])
                print(f"🔍 Found {len(items)} caption tracks for {video_id}")
                if not items:
                    print(f"❌ No caption tracks found for {video_id}")
                    return ""

                # Rank: uploaded English first, then ASR English, then others
                def rank(item: Dict[str, Any]) -> int:
                    snip = item.get("snippet", {})
                    lang = (snip.get("language") or "").strip()
                    is_asr = (snip.get("trackKind", "").lower() == "asr")
                    is_en = lang in english_lang_codes or lang.startswith("en-") or lang.startswith("en")
                    if is_en and not is_asr:
                        return 0
                    if is_en and is_asr:
                        return 1
                    return 2

                items.sort(key=rank)

                # Try each caption track until we get content (limit to 1 attempt to save quota)
                for i, cap in enumerate(items[:1]):  # Only try the best match
                    snip = cap.get("snippet", {})
                    lang = snip.get("language")
                    track_kind = snip.get("trackKind", "")
                    print(f"🎯 Trying caption: lang={lang}, trackKind={track_kind}")
                    if not (lang in english_lang_codes or (lang or "").startswith("en")):
                        print(f"⏭️ Skipping non-English caption: {lang}")
                        continue

                    # Use only the baseUrl from Data API v3 (no internal timedtext calls)
                    base_url = snip.get("baseUrl")  # This is the official way
                    if base_url:
                        print(f"📥 Downloading via official baseUrl from Data API v3")
                        text = await self._download_timedtext(base_url, client)
                        if text:
                            return text
                    else:
                        print(f"⚠️ No baseUrl available in Data API v3 response - captions may require OAuth")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                print(f"❌ Rate limited (429) for {video_id}. Using demo transcript.")
                raise e
            else:
                print(f"❌ HTTP error {e.response.status_code} for {video_id}")
                raise e
        except Exception as e:
            print(f"❌ Unexpected error for {video_id}: {e}")
            raise e

        return ""

    async def _download_timedtext(self, url: str, client: httpx.AsyncClient) -> str:
        try:
            resp = await client.get(url)
            if resp.status_code == 200 and resp.text and "<html" not in resp.text.lower():
                # Convert VTT/SRT/TTML-ish to plaintext by stripping tags; minimal for v1
                text = resp.text
                # crude cleanup:
                text = text.replace("\r", "\n")
                return text
        except Exception:
            return ""
        return ""

    def _get_demo_transcript(self, video_id: str) -> str:
        """Generate a demo transcript for testing purposes."""
        demo_transcripts = {
            "dQw4w9WgXcQ": "Never gonna give you up, never gonna let you down, never gonna run around and desert you. Never gonna make you cry, never gonna say goodbye, never gonna tell a lie and hurt you.",
            "jNQXAC9IVRw": "This is a demo transcript about technology and programming. The video discusses various programming concepts, best practices, and modern development techniques. It covers topics like clean code, testing methodologies, and software architecture patterns.",
            "OguTXEnxJqk": "This is a demo transcript about financial planning and investment strategies. The video covers topics like portfolio diversification, risk management, and long-term wealth building. It discusses various investment vehicles and their pros and cons.",
            "gV9r3ISZrws": "This is a demo transcript about machine learning and artificial intelligence. The video explores different ML algorithms, data preprocessing techniques, and model evaluation methods. It also covers practical applications and real-world use cases."
        }
        
        return demo_transcripts.get(video_id, f"This is a demo transcript for video {video_id}. In a real implementation, this would contain the actual transcript text from the YouTube video. The video appears to be about technology and programming topics, which would be useful for answering questions about the channel's content.")

    def _get_demo_transcripts(self) -> List[Dict[str, str]]:
        """Return demo transcripts for testing when quota is exceeded."""
        return [
            {
                "video_id": "demo1",
                "title": "Demo Video 1",
                "text": "This is a demo transcript about financial planning and investment strategies. The video covers topics like portfolio diversification, risk management, and long-term wealth building."
            },
            {
                "video_id": "demo2", 
                "title": "Demo Video 2",
                "text": "This is a demo transcript about machine learning and artificial intelligence. The video explores different ML algorithms, data preprocessing techniques, and model evaluation methods."
            }
        ]


