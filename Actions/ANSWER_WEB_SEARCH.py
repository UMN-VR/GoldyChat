#ANSWER_WEB_SEARCH.py file

from Memory import knowledge_log_string_without_keys, conversation_log_string, get_highest_fact_index, fact_exists
from OpenAI import call_openai_api
from prompts import web_search_pre_prompt, web_search_middle_prompt, web_search_post_prompt
from Actions.GOOGLE_SEARCH import make_google_search


def answer_web_search(server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print("Going into 'ANSWER_WEB_SEARCH' function")
    prompt = format_answer_web_search_prompt(conversation_log, knowledge_log)
    print(f"Sending prompt to OpenAI API:\n\n{prompt}\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"OpenAI API response: '{response}'")
    # Check if the response contains "NO_DATA"

    # Split response into two parts: action and message_text
    action, _, message_text = response.partition(':')

    if "NO_DATA" in response:
        return ""
    
    elif ':' in response:
        # Send the first message (message_text) if it's not empty
        process_action = lambda action, server, channel, conversation_log, knowledge_log, predefined_responses, text: __import__("actions").process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
        action_result = process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, message_text)
    
    elif action in predefined_responses:
        # Call the corresponding function for the action
        process_action = lambda action, server, channel, conversation_log, knowledge_log, predefined_responses, text: __import__("actions").process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
        action_result = process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, message_text)

    return action_result


def format_answer_web_search_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{web_search_pre_prompt}\n\"{knowledge_log_str}\n\"\n{web_search_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{web_search_post_prompt}"
    return full_prompt