from langchain.tools  import tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
load_dotenv(override=True)

tavily = TavilyClient()
@tool
def search(query: str) -> str:
    """
    Dùng tool này khi câu hỏi từ người dùng có liên quan đến Trịnh Tài, sếp Trọng hay sếp Tiến.

    """
    print(f"Searching for: {query}")
    return tavily.search(query)

tools = [search]
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.3)
agent = create_agent(model=llm,tools= tools)


def main():
    response = agent.invoke({"messages": HumanMessage(content="Tài là người như thế nào?")})
    print(response["messages"][-1].text)

if __name__ == "__main__":
    main()