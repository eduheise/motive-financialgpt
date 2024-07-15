from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()


class FinancialGPT:
    """
    A class to interact with a financial database using a language model agent.

    Attributes:
        agent_executor (Any): The agent executor for interacting with the SQL database.

    Methods:
        invoke(question: str) -> str:
            Processes the given question and returns the response from the language model agent.
    """

    def __init__(self) -> None:
        """
        Initializes the FinancialGPT class by setting up the SQL database connection
        and the language model agent.
        """
        db = SQLDatabase.from_uri(
            "postgresql+psycopg2://postgres:postgres@localhost:5432/DB"
        )
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        self.agent_executor = create_sql_agent(
            llm, db=db, agent_type="openai-tools", verbose=True
        )

    def invoke(self, question: str) -> str:
        """
        Processes the given question and returns the response from the language model agent.

        Args:
            question (str): The question to be processed by the language model agent.

        Returns:
            str: The response from the language model agent.
        """
        response = self.agent_executor.invoke({"input": question})
        return response["output"].replace("$", "\$")
