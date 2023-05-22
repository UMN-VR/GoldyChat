# Memory.py File

from pprint import pprint
from OpenAI import call_openai_api
from Prompts.summarize import summarize_pre_prompt, summarize_middle_prompt, summarize_messages_prompt
from Prompts.memorize import memorize_pre_prompt, memorize_middle_prompt, memorize_post_prompt
from OpenAI import call_openai_api
from Link import Link
from state import State
from text_colors import Colors


def update_research_log(links, action, server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    channel_id = channel.id
    new_research_log = State.channel_memory[channel_id]['research_log']
    for link in links:
        if link not in new_research_log:
            new_research_log.append(link)
    State.channel_memory[channel_id]['research_log'] = new_research_log
    return new_research_log

def research_log_string(research_log):
    research_log_dict = {}

    # Organize links by origin
    for link in research_log:
        if link.origin not in research_log_dict:
            research_log_dict[link.origin] = ""
        
        research_log_dict[link.origin] += link.title + '\n' + link.url + '\n\n' + link.summary + '\n\n'

    # Convert dictionary to string
    research_log_str = ""
    for origin, links in research_log_dict.items():
        research_log_str += 'Origin: ' + origin + '\n\n' + links + '\n\n'

    return research_log_str

def was_last_message_from_chatbot(conversation_log, chatbot_name='GoldyChat'):
    """
    This function checks if the last message in the conversation log 
    was sent by the chatbot. The conversation log is a list of dictionaries, 
    where each dictionary contains 'name' and 'content' keys.
    """
    if not conversation_log:  # If the conversation log is empty, return False
        return False
    
    # Get the last message
    last_message = conversation_log[-1]
    
    # Check if the 'name' of the sender of the last message is equal to the chatbot's name
    if last_message['name'] == chatbot_name:
        return True
    
    return False



def memory_algorithm(conversation_log, knowledge_log):
    # Implement the memory algorithm here to update conversation_log and knowledge_log
    if len(conversation_log) >= 14:
        print(f"{Colors.BRIGHT_RED}@memory_algorithm: conversation_log is too long, truncating to last 10 messages")
        # Generate a summary of the last 4 messages using the OpenAI API
        messages_to_summarize = conversation_log[-4:]
        # Format the conversation_log and knowledge_log as a string for the OpenAI API
        conversation_log = conversation_log[:-4]
        # Check if any message in messages_to_summarize contains a Link object
        for message in messages_to_summarize:
            if isinstance(message['content'], Link):
                # Call the summarize method of the Link object to set the summary attribute
                message['content'].summarize(conversation_log, knowledge_log)
        # Generate a summary of the messages_to_summarize using the OpenAI API
        summary = generate_summary(messages_to_summarize, conversation_log, knowledge_log, format_summarize_prompt)
        knowledge_log[f"earlier_info{len(knowledge_log)}"] = summary
        # Print the conversation_log and knowledge_log
        print(f"\n{Colors.BRIGHT_RED}Conversation log:")
        pprint(conversation_log)
        print("\nKnowledge log:")
        pprint(knowledge_log)
        print(f"\n{Colors.RESET}")
    


def generate_summary(messages_to_summarize, conversation_log, knowledge_log, format_summary_prompt):
    print(f"{Colors.BRIGHT_RED}@generate_summary: Generating summary of messages_to_summarize{Colors.RESET}")
    # Generate a summary of the messages_to_summarize using the OpenAI API
    prompt = format_summarize_prompt(messages_to_summarize, conversation_log,  knowledge_log)
    
    print(f"{Colors.BLUE}@generate_summary Sending Prompt to OpenAI {prompt}{Colors.RESET}")
    
    # Call OpenAI API with the generated prompt
    summary = call_openai_api(prompt, 1500)
    
    print(f"{Colors.BRIGHT_BLUE}@generate_summary Received Response from OpenAI: {summary}{Colors.RESET}")
    
    # Return the generated summary
    return summary.strip()

def format_summarize_prompt(messages_to_summarize, conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{summarize_pre_prompt}\n\"{knowledge_log_str}\n\"\n{summarize_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{summarize_messages_prompt}\n\n{conversation_log_string(messages_to_summarize)}\n\n{memorize_post_prompt}"
    return full_prompt

def fact_exists(fact_text, knowledge_log):
    for key, value in knowledge_log.items():
        if key.startswith("fact") and value.strip() == fact_text.strip():
            return True
    return False


def get_highest_fact_index(knowledge_log):
    fact_indices = [int(key[4:]) for key in knowledge_log if key.startswith("fact")]
    if fact_indices:
        return max(fact_indices)
    return -1

def knowledge_log_string_helper(knowledge_log, include_keys):
    def format_section(prefix):
        section_items = [v for k, v in knowledge_log.items() if k.startswith(prefix)]
        if include_keys:
            formatted_section = '\n'.join(f'{prefix} {i}: {item}' for i, item in enumerate(section_items))
        else:
            formatted_section = '\n'.join(section_items)
        return formatted_section

    formatted_facts = format_section('fact')
    formatted_info_about_you = format_section('info_about_you')
    formatted_earlier_info = format_section('earlier_info')

    return f"{formatted_facts}\n{formatted_info_about_you}\n{formatted_earlier_info}"

def knowledge_log_string_with_keys(knowledge_log):
    return knowledge_log_string_helper(knowledge_log, True)

def knowledge_log_string_without_keys(knowledge_log):
    return knowledge_log_string_helper(knowledge_log, False)

def conversation_log_string(conversation_log):
    conversation_history = ""
    for message in conversation_log:
        if isinstance(message['content'], Link):
            content = f"{message['content'].title} ({message['content'].url})"
        else:
            content = message['content']

        conversation_history += f"{message['name']}: {content}\n"

    return f"Conversation Log:\n{conversation_history}"
