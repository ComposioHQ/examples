from composio_llamaindex import ComposioToolSet, App, Action
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from utils import creating_connection
import os

load_dotenv()
llm = OpenAI(model='gpt-4o',api_key=os.getenv('OPENAI_API_KEY'))
composio_toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'))
creating_connection(os.getenv('ENTITY_ID'),'TAVILY',composio_toolset)
creating_connection(os.getenv('ENTITY_ID'),'GOOGLEDOCS',composio_toolset)

tools = composio_toolset.get_tools(apps = [App.TAVILY, App.GOOGLEDOCS])

prefix_messages = [
    ChatMessage(
        role="system",
        content=(
            f"""
        You are a market research agent that finds niche ideas that can be built and marketed. 
        Your users are primarily indie hackers who want to build something new and are looking for ideas. The input will 
        be a domain or a category and your job is to research extensively and find ideas that can be marketed.
        Write this content in a google doc, create a google doc before writing in it.
        I want you to show the following content:
        - Data Collection and Aggregation - Show data supporting a trend
        - Sentiment Analysis - Show customer sentiment on the topic
        - Trend Forecasting
        - Competitor Analysis
        - Competitor Benchmarking
        - Idea Validation
        First Research and then create the Google Doc with all the content
             """
        )
    )
]


agent = FunctionCallingAgentWorker(
    tools=tools,  
    llm=llm,  
    prefix_messages=prefix_messages,  
    max_function_calls=10, 
    allow_parallel_tool_calls=False,  
    verbose=True,  
).as_agent()

a = input('Enter the domain or category you want to research about:')
task = f"""
The domain or category you want to research about is {a}. Use all the tools available to you to find and gather more insights on customers and market.
"""
response = agent.chat(task)
print(response)
