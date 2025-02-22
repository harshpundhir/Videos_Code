from composio import App
from crewai_tools import ComposioTool
from crewai import Agent, Task, Crew
from composio_crewai import ComposioToolSet, App
from langchain_openai import ChatOpenAI
from pprint import pprint as pp

# Example usage

composio_toolset = ComposioToolSet(api_key="***********")
tools = composio_toolset.get_tools(
    actions=["NOTION_QUERY_DATABASE", "GOOGLECALENDAR_CREATE_EVENT"],
    entity_id="default",
)

crewai_agent = Agent(
    role="Meeting Indentifier and Google Calendar Agent",
    goal="""You are an AI agent that is responsible for finding the meeting details from the notion databse texts you have access to and add it to my google calendar""",
    backstory=(
        "You are AI agent that is responsible for finding the meeting details from the texts you have access to and add it to my google calendar"
    ),
    verbose=True,
    tools=tools,
    llm=ChatOpenAI(),
)
task = Task(
    description="""You have a Notion database ID: 1769b025447080d2bf32ca4f7e187675.
Query it to find any meeting details (title, date, start time, end time).
Then create a Google Calendar event using GOOGLECALENDAR_CREATE_EVENT with 
the parameters:
- summary
- start_time (ISO format)
- end_time (ISO format)
- any additional details
Add the event to the Google Calendar.
""",
    agent=crewai_agent,
    expected_output="All found meetings have been added to the Google Calendar",
)

my_crew = Crew(agents=[crewai_agent], tasks=[task])

result = my_crew.kickoff()
print(result)
