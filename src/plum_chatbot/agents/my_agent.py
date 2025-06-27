from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from plum_chatbot.agents.tools.vector_db import query_vector_db
from plum_chatbot.schemas.schema import Agent


class RagAgent(Agent):
    def __init__(self, name: str = "rag_agent", description: str = ""):
        self.prompt = """
Sei un assistente esperto del portale Plum, il sistema di comunicazione ufficiale del gestionale Lemon, progettato per supportare gli amministratori di condominio.

Il tuo compito è aiutare gli utenti a risolvere problemi pratici, rispondere a domande frequenti e guidarli nell’uso del portale Plum.

Prima di rispondere:
	•	Leggi con attenzione tutti i documenti forniti.
	•	Rifletti a fondo prima di scrivere una risposta.
	•	Usa uno stile chiaro, diretto e pratico.
	•	Evita invenzioni: se non sei sicuro, dì che non sai.
    •	Rispondi sempre in italiano.

Usa strumenti esterni solo se necessario e solo dopo aver analizzato tutte le informazioni disponibili. Il tuo obiettivo è fornire una risposta completa basata sui documenti e sul contesto di Plum.

Se il problema riguarda configurazioni tecniche (email, PEC, invio documenti, pagamenti digitali, integrazioni), assicurati di spiegare ogni passaggio in modo semplice ma accurato.
            """
        # Initialize the RAG agent
        self._initialize_rag_agent()
        super().__init__(
            name=name,
            description=description,
            graph=self.graph,
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

    def _initialize_rag_agent(self):
        self.llm = init_chat_model(
            "llama3.2",  # qwen3:8b
            model_provider="ollama",
            base_url="host.docker.internal",
            temperature=0.5,
        )

        self.tools = [query_vector_db]

        self.graph = create_react_agent(
            self.llm,
            self.tools,
            checkpointer=MemorySaver(),
            prompt=self.prompt,
        )


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "def234555"}}

    input_message = "come cambio la mail?"

    # for event in rag_agent.stream(
    #     {"messages": [{"role": "user", "content": input_message}]},
    #     stream_mode="values",
    #     config=config,
    # ):
    #     event["messages"][-1].pretty_print()
