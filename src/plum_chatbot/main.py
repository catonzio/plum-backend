import gradio as gr

from plum_chatbot.configs.logger import setup_logger

logger = setup_logger("application")

# Define a set of simple questions and answers
qa_pairs = {
    "What is your name?".lower(): "I am a chatbot.",
    "How are you?".lower(): "I'm doing well, thank you!",
    "What can you do?".lower(): "I can answer simple questions.",
    "Who created you?".lower(): "I was created by a developer using Gradio.",
    "Goodbye".lower(): "Goodbye! Have a nice day!",
}


def chatbot_response(message):
    logger.info(f"Received message: {message}")
    response = qa_pairs.get(
        message.strip().lower(), "Sorry, I don't understand that question."
    )
    logger.info(f"Response: {response}")

    return {"role": "assistant", "content": response}


with gr.Blocks(
    fill_height=True,
    title="Simple Chatbot",
) as demo:
    gr.Markdown("# Simple Chatbot")
    chatbot = gr.Chatbot(
        type="messages",
    )
    msg = gr.Textbox(label="Your message")
    send = gr.Button("Send")

    def respond(user_message, chat_history):
        user_msg = {"role": "user", "content": user_message}
        assistant_msg = chatbot_response(user_message)
        if chat_history is None:
            chat_history = []
        chat_history = chat_history + [user_msg, assistant_msg]
        return "", chat_history

    send.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(
        # server_name="0.0.0.0",
        # server_port=8000,
    )
