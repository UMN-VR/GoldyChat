from Memory import knowledge_log_string_without_keys, conversation_log_string
from OpenAI import call_openai_api
from Prompts.answer import answer_pre_prompt, answer_middle_prompt, answer_post_prompt
from state import State
#from actions import process_action
#from Bot import handle_simple_response
from text_colors import Colors

async def handle_response(server, channel, message, response, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@handle_response: '{response}'")

    # if State.response_done:
    #     return "DONE responding!"
    
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
        print(f"@answer_question Detected Complex response: '{message_text}' & execute {action} ")

        if action == "GoldyChat:":
            # if used username in response
            # Send response to the user if it's not empty
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)
        
        else:
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)

            if action == "ANSWER_QUESTION":
                print("@answer_question Recursion detected! aborting...") 
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
            print("@answer_question Recursion detected! aborting...") 
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

async def answer_question(server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print("@answer_question")
    prompt = format_answer_prompt(conversation_log, knowledge_log)
    print(f"{Colors.BLUE}@answer_question Sending prompt to OpenAI API:\n\n{prompt}{Colors.RESET}\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"{Colors.BRIGHT_BLUE}@answer_question OpenAI API response: {response}{Colors.RESET}\n")
    # Check if the response contains "NO_COMMENT"
    if "NO_COMMENT" in response:
        State.response_done = True
        return ""
    result = await handle_response(server, channel, text, response, conversation_log, knowledge_log, predefined_responses, text)
        
    print(f"@answer_question result: {result}")
    return result

def format_answer_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{answer_pre_prompt}\"\n{knowledge_log_str}\n\"\n{answer_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{answer_post_prompt}"
    return full_prompt
