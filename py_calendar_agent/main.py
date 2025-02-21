import os
import dotenv
import datetime
from utils import creating_connection
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.agent import FunctionCallingAgentWorker
from composio_llamaindex import Action, ComposioToolSet
dotenv.load_dotenv()

llm = OpenAI(model="gpt-4o")

composio_toolset = ComposioToolSet(api_key=os.getenv('COMPOSIO_API_KEY'), entity_id=os.getenv('ENTITY_ID'))
creating_connection(os.getenv('ENTITY_ID'), 'GOOGLECALENDAR', composio_toolset)

tools = composio_toolset.get_tools(actions=['GOOGLECALENDAR_QUICK_ADD'])

prefix_messages = [
    ChatMessage(
        role="system",
        content=(
            "You are a Calendar Agent that can schedule events"
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

date = input('Enter the date you want to schedule an event for:')
time = input('Enter the time you want to schedule an event for:')

response = agent.chat(f"This is the current date: {datetime.datetime.now()}. The user wants to schedule an event on date: {date} and time: {time}")
print("Response:", response)