import gradio as gr
import uuid
from agents.graph import part_4_graph

# Tutorial example questions
tutorial_questions = [
    "Hi there, what time is my flight?",
    "Am i allowed to update my flight to something sooner? I want to leave later today.",
    "Update my flight to sometime next week then",
    "The next available option is great",
    "what about lodging and transportation?",
    "Yeah i think i'd like an affordable hotel for my week-long stay (7 days). And I'll want to rent a car.",
    "OK could you place a reservation for your recommended hotel? It sounds nice.",
    "yes go ahead and book anything that's moderate expense and has availability.",
    "Now for a car, what are my options?",
    "Awesome let's just get the cheapest option. Go ahead and book for 7 days",
    "Cool so now what recommendations do you have on excursions?",
    "Are they available while I'm there?",
    "interesting - i like the museums, what options are there? ",
    "OK great pick one and book it for my second day there.",
]

# Maintain per-session state via Gradio's state
with gr.Blocks(title="Travel Assistant", css="""
#debug-box {overflow-y:auto; max-height:600px; padding:8px; background:#111; color:#ddd; font-size:12px; border:1px solid #333;}
.state-chip {color:#aaa; font-style:italic; margin:4px 0;}
""") as demo:
    session_thread = gr.State(str(uuid.uuid4()))
    chat_history = gr.State([])  # list of (user, ai)
    events_log = gr.State([])    # list of html strings

    gr.Markdown("# Customer Travelling Assistant")

    with gr.Row():
        with gr.Column(scale=7):
            chat = gr.Chatbot(height=500, label="Chat")
            with gr.Row():
                user_in = gr.Textbox(label="Your message", placeholder="Ask about your travel...", scale=6)
                send_btn = gr.Button("Send", variant="primary", scale=1)
            with gr.Accordion("Tutorial Example Questions", open=False):
                with gr.Row():
                    questions_dropdown = gr.Dropdown(choices=tutorial_questions, label="Select example", scale=5)
                    insert_btn = gr.Button("Insert", scale=1)
        with gr.Column(scale=3):
            gr.Markdown("### Debug Events")
            events_box = gr.HTML("<div id='debug-box'><h4>Debug Events</h4></div>")

    def process(user_msg, thread_id, history, logs):
        if not user_msg or not user_msg.strip():
            return gr.update(), thread_id, history, logs, gr.update()
        config = {
            "configurable": {"passenger_id": "3442 587242", "thread_id": thread_id},
            "recursion_limit": 25,
        }
        history = history or []
        logs = logs or []
        history.append((user_msg, None))
        events = part_4_graph.stream({"messages": ("user", user_msg)}, config, stream_mode="values")
        ai_text = ""
        for event in events:
            dialog_state = event.get("dialog_state")
            if dialog_state:
                logs.append(f"<div class='state-chip'>State: {dialog_state[-1]}</div>")
            messages = event.get("messages")
            if messages:
                last_msg = messages[-1]
                if hasattr(last_msg, 'pretty_repr'):
                    logs.append(last_msg.pretty_repr(html=True))
                content = getattr(last_msg, 'content', '')
                if isinstance(content, list):
                    # tool call style
                    text_parts = [c.get('text','') for c in content if isinstance(c, dict)]
                    content = "\n".join([p for p in text_parts if p])
                if content:
                    ai_text = content
        if history:
            history[-1] = (history[-1][0], ai_text or "")
        logs_tail = logs[-400:]
        logs_html = "<div id='debug-box'><h4>Debug Events</h4>" + "".join(logs_tail) + "</div>"
        return gr.update(value=history), thread_id, history, logs, gr.update(value=logs_html)

    send_btn.click(
        process,
        inputs=[user_in, session_thread, chat_history, events_log],
        outputs=[chat, session_thread, chat_history, events_log, events_box],
    )

    user_in.submit(
        process,
        inputs=[user_in, session_thread, chat_history, events_log],
        outputs=[chat, session_thread, chat_history, events_log, events_box],
    )

    def insert_example(q):
        return gr.update(value=q or "")

    insert_btn.click(insert_example, inputs=[questions_dropdown], outputs=[user_in])

if __name__ == "__main__":
    demo.launch()
