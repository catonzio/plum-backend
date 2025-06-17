from plum_chatbot.di_containers.datasources_containers import Container
from langchain_core.tools import tool


@tool
def query_vector_db(query: str, limit: int | None = 3) -> tuple[str, list]:
    """
    Tool to query the PLUM vector database.
    This tool uses the QdrantDatasource to perform similarity searches.
    Use this only when you need to retrieve information from the vector database, not for general queries.
    
    Args:
        query (str): The query string to search for in the vector database.
        limit (int, optional): The maximum number of results to return. Defaults to 3.
    Returns:
        tuple: A tuple containing the serialized results and the retrieved documents.
    """
    limit = limit or 3
    datasource = Container.qdrant()
    if datasource is None:
        raise ValueError("QdrantDatasource is not available in the container.")

    # def query_db(query: str, limit: int = 10):
    #     return datasource.query(query=query, limit=limit)

    retrieved_docs = datasource.query(query=query, limit=limit)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


if __name__ == "__main__":
    import asyncio

    # This is just a placeholder to prevent import errors in some environments.
    # The tool will be used in the context of an agent or a chatbot.
    print("Vector DB tool is ready to be used.")

    # print(vector_db.name)
    # print(vector_db.description)
    # print(vector_db.args)

    async def test_vector_db():
        result = query_vector_db.invoke({"query": "come cambio la mail?", "limit": 5})

        # result = amultiply.invoke({"a": 3, "b": 4})
        print(result)

    asyncio.run(test_vector_db())
