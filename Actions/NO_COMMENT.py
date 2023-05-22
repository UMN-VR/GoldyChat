from state import State

async def no_comment(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    State.response_done = True 
    print("Going into 'no_comment' function")
    return ""