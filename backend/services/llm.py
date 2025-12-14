from langchain_openai import ChatOpenAI
import os


llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aibe.mygreatlearning.com/openai/v1",
    model='gpt-4o-mini',
    temperature=0
)

ui_generation_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aibe.mygreatlearning.com/openai/v1",
    model='gpt-4o',
    temperature=0,
    streaming=True
)
