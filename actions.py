#actions.py file

from responses import predefined_responses
from summarize_list import summarize_list
from Link import Link
import inspect
from text_colors import Colors

async def process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@process_action:{action}")
    # Call the corresponding function for the action
    if action in predefined_responses:
        response_function = predefined_responses[action]
        
        if inspect.iscoroutinefunction(response_function):
            result = await response_function(server, channel, conversation_log, knowledge_log, predefined_responses, text)
        elif inspect.isfunction(response_function):
            result = response_function(server, channel, conversation_log, knowledge_log, predefined_responses, text)
        else:
            print(f"{Colors.RED}Error: Expected coroutine function for action {action}, got {type(response_function).__name__}{Colors.RESET}")
            return ""
        
        print(f"Result: {result}")
        
        if isinstance(result, list):
            # If response is a list of search results (Link objects) they need to be analyzed and a summary needs to be returned
            
            # Summarize the web research
            summary = await summarize_list(result, action, server, channel, conversation_log, knowledge_log, predefined_responses, text="")
            return summary
        else:
            # For other types of responses, return the response string
            return result
    else:
        print(f"Action Not found: {action}\n")
        return ""


