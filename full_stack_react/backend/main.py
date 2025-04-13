from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from alberto_agency import triage_agent, Runner
from trip_types import TripData
import json
import os
import requests

# uvicorn main:app --reload


class ChatRequest(BaseModel):
    user_input: str


app = FastAPI()

# Autoriser les requêtes cross-origin depuis le front local
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_context_file(session_id):
    folder_path = "context_files"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_context_name = f"conversation_context_{session_id}.json"
    context_path = os.path.join(folder_path, file_context_name)
    if not os.path.exists(context_path):
        with open(context_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"Context file created at {context_path}")


def load_context(session_id):
    folder_path = "context_files"
    file_context_name = f"conversation_context_{session_id}.json"
    context_path = os.path.join(folder_path, file_context_name)
    if os.path.exists(context_path):
        with open(context_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_context(context, session_id):
    folder_path = "context_files"
    file_context_name = f"conversation_context_{session_id}.json"
    context_path = os.path.join(folder_path, file_context_name)
    with open(context_path, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    print(f"Context saved to {context_path}")


# @app.post("/tripdata")
# async def get_trip_data(request: ChatRequest):
#     return mock_trip_data


@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}


# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     user_input = request.user_input
#     # Appel de l'agent superviseur (ou triage_agent)
#     result = await Runner.run(triage_agent, user_input)
#     print(result)
#     return {"assistant": result.final_output}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest, session_id: str):
    user_msg = {
        "role": "user",
        "content": request.user_input,
    }
    try:
        history = load_context(session_id)
        if history == []:
            raise Exception("No history available.")
        input_data = {"user_input": request.user_input, "history": history}
        print("History loaded successfully.")
        result = await Runner.run(triage_agent, str(input_data))
    except Exception as e:
        print(e)
        result = await Runner.run(triage_agent, str(request.user_input))
        history = {"messages": []}
        create_context_file(session_id)

    try:
        new_history = result.final_output.dict()
    except AttributeError:
        new_history = result.final_output
    messages_history = history.get("messages", [])
    new_history["messages"] = (
        messages_history + [user_msg] + [new_history["messages"][-1]]
    )
    save_context(new_history, session_id)
    return {"assistant": result.final_output}


@app.post("/create_session")
async def create_session_endpoint(session_id: int):
    create_context_file(session_id)
    return {"message": f"Session {session_id} created."}
