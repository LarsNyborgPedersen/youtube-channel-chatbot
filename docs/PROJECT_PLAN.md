# Project Plan: YouTube Channel Q&A (Next.js + FastAPI + LangChain + Qdrant + Ollama)

This file defines the step-by-step roadmap for building the app.  
Cursor should **only implement the current step**.  
After completing a step, mark it ✅ and update this file with the next step as “Current Step.”  

---

## Current Step
**Step 3 — Store Transcripts in Vector DB**

- Add Qdrant via Docker Compose.
- Backend endpoint `/store_transcripts`:
  - Input: transcripts.
  - Chunk, embed, store in Qdrant.
- Backend endpoint `/get_transcripts` (debugging).
- Frontend: after fetching, display transcript text in Screen 3 for confirmation.

---

## Completed Steps

✅ **Step 1 — Frontend Skeleton** *(Completed)*
- Created Next.js frontend with TypeScript, Radix UI, and TailwindCSS
- Screen 1: YouTube channel URL input with validation + "Create Chatbot" button
- Screen 2: Loading indicator with spinner animation
- Screen 3: Question input + "Ask Question" button + output area + "Back" button
- Pure UI implementation with state management for screen transitions
- Modern, responsive design with proper error handling
✅ **Step 2 — Transcript Ingestion (Backend)** *(Completed)*
- Added FastAPI backend with CORS, settings
- Endpoint `/api/transcripts/fetch`:
  - Input: YouTube channel URL.
  - Uses `youtube-transcript-api` (yt-dlp integration stubbed for now)
  - Output: JSON array of transcripts
- Frontend: Loading screen calls backend and stores transcripts
- Chat screen shows transcript preview

---

## Next Steps

**Step 4 — Refined UI Flow**
- Ensure frontend flow is final:
  - Screen 1 → Screen 2 → Screen 3.
- Show placeholder answer text (“Answer placeholder”) when asking a question.
- Back button resets state.

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
