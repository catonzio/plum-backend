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

    def __init__(self, config: PostgresParameters):
        super().__init__(name="PostgresDatasource")
        self.db_url = config.postgres_url

    async def setup(self):
        """
        Initialize the PostgreSQL client and ensure the connection is established.
        """
        self.engine = create_engine(self.db_url)
        self.session: Session = sessionmaker(bind=self.engine)()
        BaseTable.metadata.create_all(bind=self.engine)

    async def shutdown(self):
        """
        Clean up the PostgreSQL client.
        """
        self.session.close()
        self.engine.dispose()

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
