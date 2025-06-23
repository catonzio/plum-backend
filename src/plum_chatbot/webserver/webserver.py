import logging
from typing import Annotated

import uvicorn
from fastapi import APIRouter, Depends, FastAPI

from plum_chatbot.datasources.qdrant_datasource import QdrantDatasource
from plum_chatbot.di_containers.datasources_containers import Container
from plum_chatbot.ui.main import mount_gradio
from plum_chatbot.webserver.agent import router as agent_router
from plum_chatbot.webserver.lifespan import lifespan

logger = logging.getLogger(__name__)


app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/plum_chatbot", tags=["plum_chatbot"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the server is running.
    """
    return {"status": "ok"}


@router.get("/query")
async def get_query(
    datasource: Annotated[QdrantDatasource, Depends(Container.qdrant)],
    query: str = None,
):
    """
    Endpoint to retrieve the current state of the query.
    """
    return {
        "query": query,
        "results": datasource.query(query=query),
    }


app.include_router(router)
app.include_router(agent_router)

app = mount_gradio(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
