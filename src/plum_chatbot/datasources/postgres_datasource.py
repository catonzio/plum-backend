import logging
from uuid import UUID

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import Table

from plum_chatbot.datasources.base_datasource import BaseDatasource
from plum_chatbot.datasources.parameters import PostgresParameters

BaseTable = declarative_base(name="BaseTable")


class PostgresDatasource(BaseDatasource):
    """
    Datasource for PostgreSQL database.
    """

    engine: Engine
    session: Session
    db_url: str
    logger: logging.Logger

    def __init__(self, config: PostgresParameters):
        super().__init__(name="PostgresDatasource")
        self.db_url = config.postgres_url

        self.logger = logging.getLogger(__name__)

    async def setup(self):
        """
        Initialize the PostgreSQL client and ensure the connection is established.
        """
        self.engine = create_engine(self.db_url)
        self.session: Session = sessionmaker(bind=self.engine)()
        BaseTable.metadata.create_all(bind=self.engine)
        self.logger.info("PostgreSQL client initialized successfully.")

    async def shutdown(self):
        """
        Clean up the PostgreSQL client.
        """
        self.session.close()
        self.engine.dispose()
        self.logger.info("PostgreSQL client shut down successfully.")

    def query(self, query: str, params: tuple = (), **kwargs) -> Result:
        """
        Execute a query against the PostgreSQL database.

        :param query: The SQL query to execute.
        :param params: Parameters for the SQL query.
        :return: Query results.
        """
        # with self.session.begin():
        result: Result = self.session.execute(text(query), params)
        return result

    def insert(self, table: Table):
        """
        Insert a new record into the specified table.

        :param table: An instance of a SQLAlchemy model representing the table.
        """
        try:
            self.session.add(table)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def all(self, table: BaseTable):  # type: ignore
        """
        Retrieve all records from the specified table.

        :param table: An instance of a SQLAlchemy model representing the table.
        :return: List of all records in the table.
        """
        return self.session.query(table).all()

    def find(self, table: BaseTable, id: UUID):  # type: ignore
        """
        Find a record by its ID in the specified table.

        :param table: An instance of a SQLAlchemy model representing the table.
        :param id: The ID of the record to find.
        :return: The record if found, otherwise None.
        """
        return self.session.query(table).filter(table.id == id).first()

    def update(self, record: BaseTable, **kwargs):  # type: ignore
        """
        Update a record in the specified table.

        :param record: The record instance to update.
        :param kwargs: Fields to update.
        """
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            self.session.commit()
        else:
            raise ValueError("Cannot update a null record.")

    def delete(self, record: BaseTable):  # type: ignore
        """
        Delete a record from the specified table.
        """
        if record:
            self.session.delete(record)
            self.session.commit()
        else:
            raise ValueError("Cannot delete a null record.")
