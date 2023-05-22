#ANSWER_WEB_SEARCH.py file

from Memory import knowledge_log_string_without_keys, conversation_log_string, get_highest_fact_index, fact_exists
# ANSWER_WEB_SEARCH.py file

from OpenAI import call_openai_api
from Prompts.webSearch import web_search_pre_prompt, web_search_middle_prompt, web_search_post_prompt
from Actions.GOOGLE_SEARCH import make_google_search
from state import State
from text_colors import Colors

async def handle_response(server, channel, response, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@ANSWER_WEB_SEARCH_handle_response: '{response}'")

    if State.response_done:
        return "DONE responding!"
    
    if isinstance(response, list):
        print("@ANSWER_WEB_SEARCH_handle_response Detected list response")
        print("TODO handle list response")
        State.response_done = True
    
    # Use a lambda function to delay the import of process_action
    # this acts like an import statement, I think
    process_action = lambda action, server, channel, conversation_log, knowledge_log, predefined_responses, text: __import__("actions").process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
    handle_simple_response = lambda message_text, message, conversation_log, knowledge_log: __import__("Bot").handle_simple_response(message_text, channel, conversation_log, knowledge_log)

    if response in predefined_responses:
        action_result = await process_action(response, server, channel, conversation_log, knowledge_log, predefined_responses, text)
        return action_result
    
    # Split response into two parts: action and message_text
    action, _, message_text = response.partition(':')
    if ':' in response:
        print(f"@ANSWER_WEB_SEARCH_answer_question Detected Complex response: '{message_text}' & execute {action} ")
        

        if action == "GoldyChat:":
            # if used username in response
            # Send response to the user if it's not empty
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)
        
        else:
            if action == "GOOGLE_WEB_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search Google.com with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "WIKIPEDIA_WEB_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search Wikipedia.org with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "STACKOVERFLOW_WEB_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search StackOverflow.com with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "YOUTUBE_WEB_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search YouTube.com with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "GITHUB_WEB_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search GitHub.com with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "GOOGLE_MAPS_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search Google Maps with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "GOOGLE_IMAGES_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search Google Images with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "REDDIT_SEARCH":
                text = message_text # set text to message_text to be used in site search
                await handle_simple_response(f"I will search Reddit.com with the following query:{text}", channel, conversation_log, knowledge_log)
            elif action == "GIVE_UP":
                await handle_simple_response(f"I give up! I don't know how to answer that question.", channel, conversation_log, knowledge_log)
            else:
                await handle_simple_response(message_text, channel, conversation_log, knowledge_log)

            if action == "ANSWER_QUESTION":
                print("@ANSWER_WEB_SEARCH_answer_question Recursion detected! aborting...") 
                return "DONE responding!"
        
            print(f"Running: {action} text: {text}")
        
            # Call the corresponding function for the action
            action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)

            if action_result in predefined_responses:
                action_result = await process_action(action_result, server, channel, conversation_log, knowledge_log, predefined_responses, text)

            return action_result
        

    elif action in predefined_responses:
         # Call the corresponding function for the action
        print(f"Running: {action}")
        if action == "ANSWER_QUESTION":
            print("@ANSWER_WEB_SEARCH_answer_question Recursion detected! aborting...") 
            return "DONE responding!"

        action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)

        if action_result in predefined_responses:
            action_result = await process_action(action_result, server, channel, conversation_log, knowledge_log, predefined_responses, text)

        return action_result
    
    else:
        State.response_done = True
        # Send response to the user if it's not empty
        await handle_simple_response(response, channel, conversation_log, knowledge_log)
        return "DONE responding!"

async def answer_web_search(server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print("@answer_web_search")
    prompt = format_answer_web_search_prompt(conversation_log, knowledge_log)
    print(f"{Colors.BLUE}@answer_web_search Sending prompt to OpenAI API:\n\n{prompt}{Colors.RESET}\n")
    
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"{Colors.BRIGHT_BLUE}@answer_web_search OpenAI API response: '{response}'{Colors.RESET}\n")
    # Check if the response contains "NO_COMMENT" or "NO_DATA"
    if "NO_COMMENT" in response or "NO_DATA" in response:
        State.response_done = True
        return ""
    result = await handle_response(server, channel, response, conversation_log, knowledge_log, predefined_responses, text)

    print(f"@answer_web_search result: {result}")
    return result


def format_answer_web_search_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{web_search_pre_prompt}\n\"{knowledge_log_str}\n\"\n{web_search_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{web_search_post_prompt}"
    return full_prompt