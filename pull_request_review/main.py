import os
from composio_langchain import Action, App, ComposioToolSet
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from utils import creating_connection

load_dotenv()
toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
creating_connection(os.getenv('ENTITY_ID'), 'GITHUB', toolset)
tools = toolset.get_tools(apps=[App.GITHUB])

pull_request_reviewer_agent = Agent(
    role="GitHub Pull Request Reviewer",
    goal="Thoroughly review pull requests for code quality, best practices, and potential issues",
    verbose=True,
    backstory="You are an experienced software engineer specialized in code review. You analyze code changes, identify potential bugs, suggest improvements, and ensure code quality standards are met.",
    tools=list(tools),
)

pull_request_link = input('What is the link to the github pull request:')

review_pr_task = Task(
    description=f"Review the pull request at {pull_request_link}. Analyze the code changes for:\n"
                "1. Code quality and best practices\n"
                "2. Potential bugs or issues\n"
                "3. Performance implications\n"
                "4. Security concerns\n"
                "5. Documentation completeness",
    expected_output="A comprehensive review of the pull request with specific findings and recommendations.",
    agent=pull_request_reviewer_agent,
)

crew = Crew(
    agents=[pull_request_reviewer_agent],
    tasks=[review_pr_task],
    process=Process.sequential,
)

result = crew.kickoff()
print(result)
