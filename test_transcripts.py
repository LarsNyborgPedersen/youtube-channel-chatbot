#!/usr/bin/env python3
"""
Test script for transcript fetching functionality.
Run this to verify Step 2 implementation works.
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.transcripts import TranscriptService

async def test_transcript_fetching():
    """Test the transcript fetching with a real YouTube channel."""
    
    # Test with a popular channel that likely has transcripts
    test_channels = [
        "https://www.youtube.com/@3Blue1Brown",  # Educational channel with transcripts
        "https://www.youtube.com/@TED",  # TED talks usually have transcripts
        "https://www.youtube.com/@veritasium",  # Science channel
    ]
    
    service = TranscriptService()
    
    for channel_url in test_channels:
        print(f"\n🔍 Testing channel: {channel_url}")
        print("=" * 50)
        
        try:
            transcripts = await service.fetch_channel_transcripts(channel_url)
            
            print(f"✅ Found {len(transcripts)} transcripts")
            
            for i, transcript in enumerate(transcripts[:3]):  # Show first 3
                print(f"\n📹 Video {i+1}:")
                print(f"   ID: {transcript.video_id}")
                print(f"   Title: {transcript.title}")
                print(f"   Text length: {len(transcript.text)} characters")
                print(f"   Preview: {transcript.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_transcript_fetching())
