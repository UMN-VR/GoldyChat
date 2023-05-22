from state import State
from text_colors import Colors
from Prompts.feedback import feedbackAlgorithm_pre_prompt, feedbackAlgorithm_middle_prompt, feedbackAlgorithm_research_prompt, feedbackAlgorithm_post_prompt
from Memory import research_log_string, conversation_log_string, knowledge_log_string_without_keys

def format_feedbackAlgorithm_prompt(conversation_log, knowledge_log, research_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    research_log_string = research_log_string(research_log)

    full_prompt = f"{feedbackAlgorithm_pre_prompt}\"\n{knowledge_log_str}\n\"\n{feedbackAlgorithm_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{feedbackAlgorithm_research_prompt}\n\n{research_log_string}{feedbackAlgorithm_post_prompt}"
    
    return full_prompt

def feedbackAlgorithm(result, server, channel, message, conversation_log, knowledge_log):
    channel_id = channel.id
    research_log = State.channel_memory[channel_id]['research_log']

    print(f"{Colors.WHITE}@feedbackAlgorithm: result:{result}  server:{server}  channel:{channel}  message:{message}  conversation_log{conversation_log}  knowledge_log{knowledge_log}  research_log:{research_log}{Colors.RESET}")

    promt = format_feedbackAlgorithm_prompt(conversation_log, knowledge_log, research_log)


