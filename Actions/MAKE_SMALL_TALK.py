from Memory import knowledge_log_string_without_keys, conversation_log_string, was_last_message_from_chatbot
from Prompts.smallTalk import smallTalk_pre_prompt, smallTalk_middle_prompt_chatbot, smallTalk_post_prompt_chatbot, smallTalk_middle_prompt_user, smallTalk_post_prompt_user
from OpenAI import call_openai_api
from state import State
from text_colors import Colors

async def make_small_talk(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print("@make_small_talk")
    State.response_done = True
    
    # Format conversation_log and knowledge_log as the OpenAI API prompt
    prompt = format_smallTalk_prompt(server, channel, conversation_log, knowledge_log)
    print(f"\n{Colors.BLUE}Sending prompt to OpenAI API:\n'\n{prompt}\n'{Colors.RESET}\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"{Colors.BRIGHT_BLUE}@make_small_talk OpenAI API response: {response}{Colors.RESET}\n")

    action, _, message_text = response.partition(':')

    if ':' in response:
        return message_text.strip()

    # Check if the response contains "NO_COMMENT"
    if "NO_COMMENT" in response:
        State.response_done = True
        return ""

    # Return the generated response
    return response.strip()


def format_smallTalk_prompt(server, channel, conversation_log, knowledge_log):
    print(conversation_log)

    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    if (was_last_message_from_chatbot(conversation_log)):
        full_prompt = f"{smallTalk_pre_prompt}\n\"\n{knowledge_log_str}\n\"\n{smallTalk_middle_prompt_chatbot}\n\nServer:'{server}'  Channel:'#{channel}\n{conversation_log_string(conversation_log)}\n\n{smallTalk_post_prompt_chatbot}"
    else:
        full_prompt = f"{smallTalk_pre_prompt}\n\"\n{knowledge_log_str}\n\"\n{smallTalk_middle_prompt_user}\n\nServer:'{server}'  Channel:'#{channel}\n{conversation_log_string(conversation_log)}\n\n{smallTalk_post_prompt_user}"

    
    return full_prompt