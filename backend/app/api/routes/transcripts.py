from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from ...services.transcripts import TranscriptService

router = APIRouter(prefix="/transcripts", tags=["transcripts"])


class FetchTranscriptsRequest(BaseModel):
    channel_url: HttpUrl


class TranscriptItem(BaseModel):
    video_id: str
    title: str
    text: str


class FetchTranscriptsResponse(BaseModel):
    transcripts: list[TranscriptItem]


@router.post("/fetch", response_model=FetchTranscriptsResponse)
async def fetch_transcripts(payload: FetchTranscriptsRequest) -> FetchTranscriptsResponse:
    try:
        service = TranscriptService()
        items = await service.fetch_channel_transcripts(channel_url=str(payload.channel_url))
        return FetchTranscriptsResponse(transcripts=items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:  # pragma: no cover - unexpected
        raise HTTPException(status_code=500, detail="Failed to fetch transcripts") from e


