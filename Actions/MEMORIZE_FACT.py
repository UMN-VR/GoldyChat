from Memory import knowledge_log_string_without_keys, conversation_log_string, get_highest_fact_index, fact_exists
from OpenAI import call_openai_api
from Prompts.memorize import memorize_pre_prompt, memorize_middle_prompt, memorize_post_prompt
from text_colors import Colors

async def memorize_fact(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print("@memorize_fact")
    prompt = format_memorize_prompt(conversation_log, knowledge_log)
    print(f"{Colors.BLUE}Sending prompt to OpenAI API:\n\n{prompt}\n{Colors.RESET}")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"{Colors.BRIGHT_BLUE}@memorize_fact OpenAI API response: {response}{Colors.RESET}")
    # Check if the response contains "NO_DATA"
    if "NO_DATA" in response:
        return ""
    
    # Split the response into lines
    response_lines = response.strip().split('\n')

    # Get the highest fact index in the knowledge log
    highest_fact_index = get_highest_fact_index(knowledge_log)

    # Iterate through the lines and extract the facts
    for line in response_lines:
        if line.startswith("fact"):
            fact_key, fact_text = line.split(":", 1)
            # Check if the fact is already in the knowledge log
            if not fact_exists(fact_text.strip(), knowledge_log):
                highest_fact_index += 1
                fact_key = f"fact{highest_fact_index}"
                knowledge_log[fact_key] = fact_text.strip()

    # Return an empty string since we are updating the knowledge log directly
    return ""


def format_memorize_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{memorize_pre_prompt}\n\"{knowledge_log_str}\n\"\n{memorize_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{memorize_post_prompt}"
    return full_prompt