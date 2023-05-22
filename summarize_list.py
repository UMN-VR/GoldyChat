from summarizeWebResults import summarize_web_research
from Memory import update_research_log

async def summarize_list(list, action, server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    research_log = update_research_log(list, action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
    result = await summarize_web_research(research_log, action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
    return result