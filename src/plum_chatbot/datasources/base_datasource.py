from abc import ABC


class BaseDatasource(ABC):
    """
    Base class for all data sources.
    This class should be inherited by any data source that needs to implement specific methods.
    """

    def __init__(self, name: str, config: dict | None = None):
        """
        Initialize the base data source with a name.

        :param name: The name of the data source.
        """
        self.name = name
        # self.config = config

    def setup(self):
        """
        Method to initialize the data source.
        Should be implemented by subclasses.

        :return: None
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def shutdown(self):
        """
        Method to clean up the data source.
        Should be implemented by subclasses.

        :return: None
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def query(self, query: str, limit: int = 10):
        """
        Method to query the data source.
        Should be implemented by subclasses.

        :param query: The query string to execute.
        :param limit: The maximum number of results to return.
        :return: Query results.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    async def aquery(self, query: str, limit: int = 10):
        """
        Method to asynchronously query the data source.
        Should be implemented by subclasses.
        :param query: The query string to execute.
        :param limit: The maximum number of results to return.
        :return: Query results.
        """
        raise NotImplementedError("Subclasses must implement this method.")
