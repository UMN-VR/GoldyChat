#actions.py file

from responses import predefined_responses


async def process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@In process_action:{action}")
    # Call the corresponding function for the action
    if action in predefined_responses:
        response_function = predefined_responses[action]
        response = response_function(server, channel, conversation_log, knowledge_log, predefined_responses, text)
        if isinstance(response, list):
            # If response is a list of search results (Link objects), return it as is
            return response
        else:
            # For other types of responses, return the response string
            return response
    else:
        print(f"Action Not found: {action}\n")
        return ""


