from Memory import knowledge_log_string_without_keys, conversation_log_string
from prompts import smallTalk_pre_prompt, smallTalk_middle_prompt, smallTalk_post_prompt
from OpenAI import call_openai_api

def make_small_talk(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print("Going into 'make_small_talk' function")
    
    # Format conversation_log and knowledge_log as the OpenAI API prompt
    prompt = format_smallTalk_prompt(server, channel, conversation_log, knowledge_log)
    print(f"\nSending prompt to OpenAI API:\n'\n{prompt}\n'\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"OpenAI API response: {response}")

    action, _, message_text = response.partition(':')

    if ':' in response:
        return message_text.strip()

    # Check if the response contains "NO_COMMENT"
    if "NO_COMMENT" in response:
        return ""
    
    # Return the generated response
    return response.strip()


def format_smallTalk_prompt(server, channel, conversation_log, knowledge_log):
    print(conversation_log)
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{smallTalk_pre_prompt}\n\"{knowledge_log_str}\n\"\n{smallTalk_middle_prompt}\n\nServer:'{server}'  Channel:'#{channel}\n{conversation_log_string(conversation_log)}\n\n{smallTalk_post_prompt}"
    return full_prompt