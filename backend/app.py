from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json
import time
import jsonpatch   # pip install jsonpatch
import pickle
import pandas as pd
from pydantic import BaseModel
# from llm_utils import structured_ui_gen_llm, messages

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

DATA_REGISTRY = {}
BACKGROUND_JOBS = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_chunks():
    with open("ui_spec_stream_news.json") as f:
        return json.load(f)


# load data registry from pickle file into memory
def load_data_registry():
    global DATA_REGISTRY
    try:
        with open("data_registry.pkl", "rb") as f:
            DATA_REGISTRY = pickle.load(f)
    except FileNotFoundError:
        DATA_REGISTRY = {}


load_data_registry()


@app.get("/")
def read_root():
    return {"message": "UI Spec Replay Service is running."}


# ============================================================
# 1️⃣ FULL UI SPEC STREAM (SSE) — WITH SPEED CONTROL
# ============================================================
@app.get("/ui_stream_replay")
def replay_ui_stream(request: Request, speed: float = 1.0):
    """
    Replays the full UISpec chunks in streaming mode.
    Speed > 1.0 = faster, < 1 = slower.
    """

    chunks = load_chunks()

    # Base delay between events (customizable)
    base_delay = 0.2
    delay = base_delay / speed

    def event_stream():
        for chunk in chunks:
            data = json.dumps(chunk)
            yield f'data: {json.dumps({"type": "patch", "patch": data})}\n\n'
            time.sleep(delay)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ============================================================
# 2️⃣ PATCH STREAM (SSE) — STREAM ONLY DIFFS
# ============================================================
@app.get("/ui_stream_patch")
def replay_ui_stream_patch(request: Request, speed: float = 1.0):
    """
    Streams JSON Patch diffs instead of full UI spec.
    Perfect for efficient frontend updates.
    """

    chunks = load_chunks()

    base_delay = 0.2
    delay = base_delay / speed

    def patch_stream():
        prev = None

        for curr in chunks:
            if prev is None:
                # First chunk: send full object
                patch = [{"op": "replace", "path": "", "value": curr}]

            else:
                # Generate JSON Patch (RFC 6902)
                patch = jsonpatch.make_patch(prev, curr).patch

            yield f'data: {json.dumps({"type": "patch", "patch": patch})}\n\n'
            prev = curr
            time.sleep(0.1)
        yield "event: end\ndata: done\n\n"

    return StreamingResponse(patch_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "close"})


# route to read data registry based on key
@app.get("/data_registry/{key}")
def read_data_registry(key: str):
    """
    Reads data from the data registry based on the provided key.
    """
    global DATA_REGISTRY
    value = DATA_REGISTRY.get(key)
    if value is None:
        return {"error": "Key not found in data registry."}
    value = value.to_dict(orient="records")
    return {"key": key, "value": value}


# post route that accepts user prompt which returns a job id. The job id is a uuid4 string.
class PromptRequest(BaseModel):
    prompt: str


@app.post("/submit_prompt")
def submit_prompt(request: PromptRequest):
    """
    Accepts a user prompt and returns a job ID.
    """
    import uuid

    job_id = str(uuid.uuid4())

    # Use request.prompt instead of prompt
    BACKGROUND_JOBS[job_id] = {"status": "submitted", "prompt": request.prompt}

    return {"job_id": job_id, "prompt": request.prompt}


# route to streaming response that simulates background job progress
@app.get("/trigger_job/{job_id}")
def job_status(request: Request, job_id: str):
    """
    Streams job status updates for the given job ID.
    """

    chunks = load_chunks()

    base_delay = 0.2
    delay = base_delay / 1.0

    def patch_stream():

        # yield f"data: {{\"status\": \"Job {job_id} started.\"}}\n\n"
        # time.sleep(1.0)

        # yield f"data: {{\"status\": \"Processing prompt...\"}}\n\n"
        # time.sleep(1.0)

        # yield f"data: {{\"status\": \"Generating UI spec...\"}}\n\n"

        yield f"data: {json.dumps({'type': 'status', 'message': f'Job {job_id} started...'})}\n\n"
        time.sleep(1.0)

        yield f"data: {json.dumps({'type': 'status', 'message': f'Generating UI spec...'})}\n\n"
        time.sleep(1.0)

        yield f"data: {json.dumps({'type': 'status', 'message': f'Streaming UI spec...'})}\n\n"

        prev = None

        # for chunk in structured_ui_gen_llm.stream(messages):

        # curr = chunk.model_dump()
        for curr in chunks:
            if prev is None:
                # First chunk: send full object
                patch = [{"op": "replace", "path": "", "value": curr}]

            else:
                # Generate JSON Patch (RFC 6902)
                patch = jsonpatch.make_patch(prev, curr).patch

            yield f'data: {json.dumps({"type": "patch", "patch": patch})}\n\n'
            prev = curr
            time.sleep(0.1)
        yield "event: end\ndata: done\n\n"

    return StreamingResponse(patch_stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "close"})
