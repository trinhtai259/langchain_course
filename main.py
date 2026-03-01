from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAI
from transformers import AutoTokenizer, AutoModelForCausalLM

load_dotenv()

loader = PyPDFLoader("C:\AI_Engineer\legal_chatbot\data\luat_an_ninh_mang.pdf")
pages = loader.load_and_split()
information = pages[0].page_content
summary_template = """
Bạn là một trợ lý hữu ích tóm tắt nội dung của tài liệu PDF.

Đây là nội dung của tài liệu PDF: {information}
Vui lòng cung cấp bản tóm tắt ngắn gọn các điểm chính và thông tin quan trọng từ tài liệu."""
summary = PromptTemplate.from_template( template=summary_template)

llm = GoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.3)

chain = summary | llm
response = chain.invoke(input={'information':information})
def main():
    print(response)


if __name__ == "__main__":
    main()
