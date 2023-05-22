
from Link import Link
from OpenAI import call_openai_api
from state import State
from Prompts.summarizeWeb import summarize_web_pre_prompt, summarize_web_conversation_prompt, summarize_web_research_prompt, summarize_web_post_prompt
from Memory import knowledge_log_string_without_keys, conversation_log_string, research_log_string
from text_colors import Colors


async def handle_response(server, channel, message, response, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@summarize_web_research_handle_response: '{response}'")

    if State.response_done:
        return "DONE responding!"
    
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
        print(f"@summarize_web_research_handle_response Detected Complex response: '{message_text}' & execute {action} ")

        if action == "GoldyChat:":
            # if used username in response
            # Send response to the user if it's not empty
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)
        
        else:
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)

            if action == "ANSWER_QUESTION":
                print("@summarize_web_research_handle_response Recursion detected! aborting...") 
                return "DONE responding!"
        
            print(f"Running: {action}")
        
            # Call the corresponding function for the action
            action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)

            if action_result in predefined_responses:
                action_result = await process_action(action_result, server, channel, conversation_log, knowledge_log, predefined_responses, text)

            return action_result
        

    elif action in predefined_responses:
         # Call the corresponding function for the action
        print(f"Running: {action}")
        if action == "ANSWER_QUESTION":
            print("@summarize_web_research_handle_response Recursion detected! aborting...") 
            return "DONE responding!"

        action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)

        if action_result in predefined_responses:
            action_result = await process_action(action_result, server, channel, conversation_log, knowledge_log, predefined_responses, text)

        return action_result

    else:
        State.response_done = True
        # Send response to the user if it's not empty
        await handle_simple_response(response, message, conversation_log, knowledge_log)
        return "DONE responding!"

async def summarize_web_research(research_log, action, server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@summarize_web_research: {research_log}")



    print("Summarizing web research...")
    prompt = format_webResearch_prompt(research_log, conversation_log, knowledge_log)
    print(f"{Colors.BLUE}@summarize_web_research Sending prompt to OpenAI API:\n\n{prompt}{Colors.RESET}\n")

    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"{Colors.BRIGHT_BLUE}@summarize_web_research OpenAI API response: {response}{Colors.RESET}\n")
    # Check if the response contains "NO_COMMENT"
    if "NO_COMMENT" in response:
        State.response_done = True
        return ""
    result = await handle_response(server, channel, text, response, conversation_log, knowledge_log, predefined_responses, text)
        
    print(f"@summarize_web_research result: {result}")
    return result

def format_webResearch_prompt(research_log, conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    research_log_string = research_log_string(research_log)
    full_prompt = f"{summarize_web_pre_prompt}\"\n{knowledge_log_str}\n\"\n{summarize_web_conversation_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{summarize_web_research_prompt}\n\n{research_log_string}{summarize_web_post_prompt}"
    return full_prompt
