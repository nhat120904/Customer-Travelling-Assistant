import shutil
import uuid
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from db import update_dates
from agents.graph import part_4_graph
from utils.utils import _print_event
from langchain_core.messages import ToolMessage
import json

load_dotenv()

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

# Initialize variables
db = "travel2.sqlite"
db = update_dates(db)

# Helper function to process events
def process_event(event, printed, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        state = current_state[-1]
    else:
        state = ""

    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in printed:
            msg_repr = message.pretty_repr(html=False)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            printed.add(message.id)
            return {
                "state": state,
                "message": msg_repr,
            }
    return {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # count = 0
    await manager.connect(websocket)
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            "passenger_id": "3442 587242",
            "thread_id": thread_id,
        },
        "recursion_limit": 25,
    }

    printed_messages = set()

    try:
        while True:
            user_message = await websocket.receive_text()

            # Stream the response from the graph
            events = part_4_graph.stream(
                {"messages": ("user", user_message)}, config, stream_mode="values"
            )

            for event in events:
                processed_event = process_event(event, printed_messages)
                if processed_event:
                    await manager.broadcast({
                        "type": "event",
                        "state": processed_event["state"],
                        "message": processed_event["message"],
                        # "id": count,
                    })

            # Handle state transitions
            snapshot = part_4_graph.get_state(config)
            while snapshot.next:
                # await websocket.send_text("{'message': 'Ai Message\n\nDo you approve of the above actions? (y/n):'}")
                await websocket.send_text(json.dumps({
                    "message": 'Ai Message\n\nDo you approve of the above actions? (y/n):'
                }))
                user_input = await websocket.receive_text()

                # print(user_input)

                if user_input.lower() == "y":
                    # Continue processing
                    result = part_4_graph.invoke(None, config)
                else:
                    tool_messages = [
                        ToolMessage(
                            tool_call_id=tc["id"],
                            content=f"API call denied by user. Reasoning: '{user_input}'. Continue assisting, accounting for the user's input."
                        )
                        for tc in event["messages"][-1].tool_calls
                    ]

                    result = part_4_graph.invoke({"messages": tool_messages}, config)
                await websocket.send_text(json.dumps({
                    "message":  f'Ai Message\n\n{result["messages"][-1].content}'
                }))
                
                snapshot = part_4_graph.get_state(config)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "WebSocket Server Running. Connect via /ws."}
