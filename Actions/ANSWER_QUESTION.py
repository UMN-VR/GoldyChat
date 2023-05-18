from Memory import knowledge_log_string_without_keys, conversation_log_string
from OpenAI import call_openai_api
from prompts import answer_pre_prompt, answer_middle_prompt, answer_post_prompt

def answer_question(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print("Going into 'answer_question' function")
    prompt = format_answer_prompt(conversation_log, knowledge_log)
    print(f"Sending prompt to OpenAI API:\n\n{prompt}\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"OpenAI API response: {response}")
    # Check if the response contains "NO_COMMENT"
    if "NO_COMMENT" in response:
        return ""

    # Use a lambda function to delay the import of process_action
    process_action = lambda action, conversation_log, knowledge_log, predefined_responses: __import__("actions").process_action(action, conversation_log, knowledge_log, predefined_responses)

    if response in predefined_responses:
        action_result = process_action(response.strip(), conversation_log, knowledge_log, predefined_responses)
        return action_result.strip()
    elif ':' in response:
        # Split response into two parts: action and message_text
        action, _, message_text = response.partition(':')
        
        # Call the corresponding function for the action
        action_result = process_action(action.strip(), conversation_log, knowledge_log, predefined_responses)
        
        return action_result.strip()
    else:
        return response.strip()

def format_answer_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{answer_pre_prompt}\"\n{knowledge_log_str}\n\"\n{answer_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{answer_post_prompt}"
    return full_prompt
