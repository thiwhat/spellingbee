"""
Spelling Bee Trainer — Web Backend
FastAPI server: serves CSV word lists and streams edge-tts audio
"""
import asyncio, io, csv, os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WORD_FILES = {
    "general": os.path.join(BASE_DIR, "words.csv"),
    "trap":    os.path.join(BASE_DIR, "trap_words.csv"),
    "final":   os.path.join(BASE_DIR, "final_round_words.csv"),
}

EDGE_VOICE = "en-US-AvaMultilingualNeural"


def load_csv(path: str) -> list:
    words = []
    if not os.path.exists(path):
        return words
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            clean = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            if clean.get("word"):
                words.append({
                    "word":           clean.get("word", "").lower(),
                    "grade":          clean.get("grade_level", "3"),
                    "difficulty":     clean.get("difficulty", "easy").lower(),
                    "definition":     clean.get("definition", ""),
                    "sentence":       clean.get("sentence", ""),
                    "part_of_speech": clean.get("part_of_speech", ""),
                    "origin":         clean.get("origin", ""),
                })
    return words


# ── Word list endpoints ────────────────────────────────────────────────────────
@app.get("/api/words/{set_key}")
def get_words(set_key: str):
    if set_key not in WORD_FILES:
        raise HTTPException(status_code=404, detail="Unknown word set")
    return load_csv(WORD_FILES[set_key])


# ── TTS endpoint ───────────────────────────────────────────────────────────────
class TTSRequest(BaseModel):
    text: str
    rate: str = "-10%"


@app.post("/api/tts")
async def tts(req: TTSRequest):
    try:
        import edge_tts
        buf = io.BytesIO()

        async def _synth():
            comm = edge_tts.Communicate(req.text, EDGE_VOICE, rate=req.rate)
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])

        if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        loop = asyncio.new_event_loop()
        loop.run_until_complete(_synth())
        loop.close()

        buf.seek(0)
        return StreamingResponse(buf, media_type="audio/mpeg")

    except ImportError:
        raise HTTPException(status_code=503, detail="edge-tts not installed")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Serve frontend ─────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
