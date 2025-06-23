import logging

import gradio as gr
from fastapi import FastAPI

from plum_chatbot.agents.agents import invoke_chatbot
from plum_chatbot.configs.settings import Settings
from plum_chatbot.datasources.base_datasource import BaseDatasource
from plum_chatbot.datasources.models.chat_message import ChatMessage as DBChatMessage
from plum_chatbot.di_containers.datasources_containers import Container, container
from plum_chatbot.schemas.schema import ChatMessage, UserInput

logger = logging.getLogger(__name__)


def mount_gradio(app: FastAPI) -> FastAPI:
    """
    Mount the Gradio app on the FastAPI app.
    This function is used to mount the Gradio app that will be served by FastAPI.
    """
    demo = gradio_app()
    app = gr.mount_gradio_app(app, demo, path="/gradio")
    return app


async def ask_chatbot(message, history, state):
    # Always respond with "yes" as a message tuple (user, bot)
    # history = history or []
    # history.append((message, "yes"))
    logger.info(f"Received message: {message}")
    response: ChatMessage = await invoke_chatbot(
        UserInput(message=message), Settings().DEFAULT_AGENT
    )
    db_message: DBChatMessage = DBChatMessage(
        chat_id=response.thread_id,
        question=message,
        answer=response.content,
    )
    Container.postgres().insert(db_message)
    # if not state("thread_id", None):
    #     logger.info("No thread_id found in state, setting it now.")
    #     state["thread_id"] = response.thread_id
    # logger.info(f"Thread ID: {state['thread_id']}")
    return response.content


def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: " + data.value[0])
    else:
        print("You downvoted this response: " + data.value[0])


def gradio_app() -> gr.Blocks:
    """
    Create a Gradio app instance.
    This function is used to create the Gradio app that will be mounted on the FastAPI app.
    """

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(
            placeholder="<strong>Il tuo assistente personale</strong><br>Chiedimi qualsiasi cosa",
            type="messages",
            max_height=None,
            render_markdown=True,
            show_copy_button=True,
            sanitize_html=True,
            min_height=600,
        )
        chatbot.like(vote, None, None)
        gr.State({})

        gr.ChatInterface(
            fn=ask_chatbot,
            chatbot=chatbot,
            stop_btn=True,
            show_progress=True,
            title="Plum Chatbot",
            type="messages",
            # description="Un'interfaccia chatbot semplice che utilizza Gradio.",
            examples=[
                "Come posso aggiornare la mia email?",
                "Come posso aggiornare la pec?",
            ],
            fill_height=True,
            fill_width=True,
        )
    return demo


if __name__ == "__main__":
    try:
        container.init_resources()
        for k, v in Container.providers.items():
            provider = v()
            if isinstance(provider, BaseDatasource):
                provider.setup()
        gradio_app().launch(server_name="0.0.0.0", server_port=7860)
    finally:
        for k, v in Container.providers.items():
            provider = v()
            if isinstance(provider, BaseDatasource):
                provider.shutdown()
        container.shutdown_resources()
