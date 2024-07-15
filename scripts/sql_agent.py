from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

db = SQLDatabase.from_uri("postgresql+psycopg2://postgres:postgres@localhost:5432/DB")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

response = agent_executor.invoke(
    {"input": "Which assets composes the portfolio from client number 23?"}
)
print(response)
