# Project Plan: YouTube Channel Q&A (Next.js + FastAPI + LangChain + Qdrant + Ollama)

This file defines the step-by-step roadmap for building the app.  
Cursor should **only implement the current step**.  
After completing a step, mark it ✅ and update this file with the next step as “Current Step.”  

---

## Current Step
**Step 1 — Frontend Skeleton**

- Create a Next.js frontend.
- Screen 1: Input box for YouTube channel URL + "Create Chatbot" button.
- On click, transition to Screen 2 (loading indicator).
- Screen 3: Input box for a question + "Ask Question" button + output area + "Back" button at top.
- At this stage, nothing connects to backend. Pure UI only.

---

## Next Steps

**Step 2 — Transcript Ingestion (Backend)**
- Add FastAPI backend.
- Endpoint `/fetch_transcripts`:
  - Input: YouTube channel URL.
  - Use `yt-dlp` to list video IDs.
  - Use `youtube-transcript-api` to fetch transcripts.
  - Output: JSON array of transcripts.
- Frontend: on "Create Chatbot", call `/fetch_transcripts`.
- Show loading spinner until finished.
- After complete, display transcript text in Screen 3 for confirmation.

---

**Step 3 — Store Transcripts in Vector DB**
- Add Qdrant via Docker Compose.
- Backend endpoint `/store_transcripts`:
  - Input: transcripts.
  - Chunk, embed, store in Qdrant.
- Backend endpoint `/get_transcripts` (debugging).
- Frontend: after fetching, display transcript text in Screen 3 for confirmation.

---

**Step 4 — Refined UI Flow**
- Ensure frontend flow is final:
  - Screen 1 → Screen 2 → Screen 3.
- Show placeholder answer text (“Answer placeholder”) when asking a question.
- Back button resets state.

---

**Step 5 — Retrieval Without LLM**
- Backend endpoint `/retrieve`:
  - Input: question.
  - Embed query, search Qdrant top-k, return chunks.
- Frontend: when asking, display retrieved chunks instead of placeholder.
- Confirms retrieval works.

---

**Step 6 — Add LLM + LangChain**
- Backend endpoint `/ask`:
  - Input: question.
  - Use LangChain RetrievalQA.
  - Retriever: Qdrant.
  - LLM: Ollama provider.
  - Output: answer string.
- Frontend: display real answer instead of chunks.

---

**Step 7 — Polish Demo**
- Add context preview (optional).
- Add loading states when asking a question.
- Ensure Back button works cleanly.
- Clean up Docker Compose: frontend + backend + qdrant + ollama.

---

## Later Enhancements (not for v1)
- Add Temporal for ingestion workflows and periodic sync.
- Add support for multiple vector DBs (Chroma, Weaviate).
- Add support for multiple LLMs (OpenAI, Anthropic).
- Implement streaming responses instead of plain text.
- Wrap in Electron/Tauri for offline desktop app.
