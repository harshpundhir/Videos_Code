
from composio import ComposioToolSet, App, action
from composio_crewai import ComposioToolSet as ComposioToolSetCrewAI
import typing as t
user_id = "pundhirharsh6@gmail.com"
app_name = "notion"
auth_scheme = "OAUTH2"


toolset = ComposioToolSet(api_key="d5k4ltozoe8voejzwtltyc")

connection_request = toolset.initiate_connection(
    app=app_name,
    redirect_url = 'https://www.google.co.uk/', # user comes here after oauth flow
    entity_id=user_id,
    auth_scheme=auth_scheme,
)

# replace connection_request_id from earlier response validate the connection is active
connected_account = toolset.get_connected_account(id=connection_request.connectedAccountId)
print(connected_account.status)  # should be active

@action(toolname="notion")
def my_custom_action(param1: str, param2: str, execute_request: t.Callable) -> str:
    """
    my custom action description which will be passed to llm

    :param param1: param1 description which will be passed to llm
    :param param2: param2 description which will be passed to llm
    :return info: return description
    """

    response = execute_request(
        "/NOTION_QUERY_DATABASE",
        "GET",
        {'database_id': '1769b025447080d2bf32ca4f7e187675'} # body can be added here
    )    # execute requests by appending credentials to the request
    return str(response) # complete auth dict is available for local use if needed

# print(my_custom_action)
toolset = ComposioToolSetCrewAI(entity_id="pundhirharsh6@gmail.com")
tools = toolset.get_tools(actions=[my_custom_action])
print(tools)