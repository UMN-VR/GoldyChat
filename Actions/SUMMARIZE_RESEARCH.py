from state import State

async def summarize_research(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print(f"@summarize_research: {text}")
    result = text
    State.response_done = True
    return result