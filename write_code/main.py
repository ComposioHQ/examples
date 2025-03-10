import os
from composio_langchain import Action, App, ComposioToolSet
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()
toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
tools = toolset.get_tools(apps=[App.CODEINTERPRETER])

python_executor_agent = Agent(
    role="Python Code Executor",
    goal="Execute Python code in a Jupyter notebook cell and return the results.",
    verbose=True,
    backstory="You are an expert in executing Python code and interpreting results in a sandbox environment.",
    tools=list(tools),
)

python_code =  input('What do you want to write code for:')


execute_code_task = Task(
    description="Execute the following Python code and return the results:\n\n"+ python_code,
    expected_output="Execution of Python code returned the results.",
    agent=python_executor_agent,
)

crew = Crew(
    agents=[python_executor_agent],
    tasks=[execute_code_task],
    process=Process.sequential,
)

result = crew.kickoff()
print(result)
