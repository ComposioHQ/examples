import os
from dotenv import load_dotenv
from composio_llamaindex import App, ComposioToolSet
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
from utils import creating_connection
from pathlib import Path
import sys 


load_dotenv()

print(os.getenv('ENTITY_ID'))
composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"), entity_id=os.getenv('ENTITY_ID'))
creating_connection(os.getenv('ENTITY_ID'),'GOOGLESHEETS',composio_toolset)
tools = composio_toolset.get_tools(apps=[App.GOOGLESHEETS], entity_id=os.getenv('ENTITY_ID'))

llm = OpenAI(model="gpt-4o", api_key=os.environ['OPENAI_API_KEY'])

print('Enter the sheet link:')
sheet_url = sys.stdin.readline() 

print("Enter the task you want to perform (or type 'exit' to quit): ")
task = sys.stdin.readline()
prefix_messages = [
    ChatMessage(
        role="system",
        content=(
            "You are an AI Agent connected with google sheets. You can perform various actions on the sheets."
            "The sheet link will be given to you, based on that extract the sheet id."
        ),
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

response = agent.chat(f"On this sheet at link:{sheet_url}, perform the following action:{task}")
print("Response:", response)