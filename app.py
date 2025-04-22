import streamlit as st
import uuid
from agents.graph import part_4_graph
from langchain_core.messages import ToolMessage

# Initialize Variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Store user and AI messages
if "debug_logs" not in st.session_state:
    st.session_state["debug_logs"] = []  # Store debug logs

thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "passenger_id": "3442 587242",
        "thread_id": thread_id,
    },
    "recursion_limit": 25,
}

# Function to Append Messages to Chat
def append_message(role, content):
    st.session_state["messages"].append({"role": role, "content": content})

# Function to Append Debug Logs
def append_debug_log(log):
    st.session_state["debug_logs"].append(log)

# Debug Log Formatter
def _print_event(event, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        append_debug_log(f"**Currently in:** {current_state[-1]}")
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        msg_repr = getattr(message, "pretty_repr", lambda html: str(message))(html=True)
        if len(msg_repr) > max_length:
            msg_repr = msg_repr[:max_length] + " ... (truncated)"
        append_debug_log(msg_repr)

# Main Chat Interface
st.title("AI Chat with Debug Console")

# Chat Message Input
user_input = st.text_input("Enter your message:", key="user_input")

if st.button("Send"):
    if user_input.strip():
        append_message("user", user_input)  # Display user message
        events = part_4_graph.stream(
            {"messages": ("user", user_input)}, config, stream_mode="values"
        )
        # Process AI responses and debug information
        for event in events:
            _print_event(event)  # Log debug information
            
            if "messages" in event:  # Check for messages in the event
                last_message = event["messages"][-1]  # Get the last message
                
                # Handle AI and tool messages
                if hasattr(last_message, "content"):  # Ensure message has 'content'
                    ai_message = last_message.content
                    append_message("ai", ai_message)  # Append AI message to chat
                else:
                    # Log an unexpected message type
                    append_debug_log(f"Unexpected message type: {type(last_message)}")



# Display Chat Interface
st.subheader("Chat")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "ai":
        st.markdown(f"**AI:** {msg['content']}")

# Debug Console
st.subheader("Debug Console")
for log in st.session_state["debug_logs"]:
    st.markdown(log, unsafe_allow_html=True)
