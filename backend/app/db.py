import os
from contextlib import contextmanager
from typing import Any, Generator
from neo4j import GraphDatabase, Driver, Session, Result
from neo4j.exceptions import ServiceUnavailable, AuthError
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


class Neo4jClient:
    _instance: "Neo4jClient | None" = None
    _driver: Driver | None = None

    def __new__(cls) -> "Neo4jClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self) -> None:
        if self._driver is not None:
            return
        try:
            self._driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
            )
            self._driver.verify_connectivity()
            print(f"Conectado a Neo4j Aura: {NEO4J_URI}")
        except AuthError as e:
            raise RuntimeError(f"Credenciales Inválidas: {e}") from e
        except ServiceUnavailable as e:
            raise RuntimeError(f"Neo4j No Disponible: {NEO4J_URI}: {e}") from e

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()
            self._driver = None

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        if self._driver is None:
            raise RuntimeError("Driver Neo4j No Inicializado, Llamar connect() Primero")
        session = self._driver.session(database=NEO4J_DATABASE)
        try:
            yield session
        finally:
            session.close()

    def run_query(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict]:
        with self.session() as session:
            result: Result = session.run(cypher, params or {})
            return [record.data() for record in result]

    def run_write(self, cypher: str, params: dict[str, Any] | None = None) -> dict:
        with self.session() as session:
            def _tx(tx, cypher: str, params: dict):
                result = tx.run(cypher, params)
                records = [r.data() for r in result]
                summary = result.consume()
                return {
                    "records": records,
                    "counters": {
                        "nodes_created": summary.counters.nodes_created,
                        "nodes_deleted": summary.counters.nodes_deleted,
                        "relationships_created": summary.counters.relationships_created,
                        "relationships_deleted": summary.counters.relationships_deleted,
                        "properties_set": summary.counters.properties_set,
                        "labels_added": summary.counters.labels_added,
                    },
                }
            return session.execute_write(_tx, cypher, params or {})


db = Neo4jClient()