from Bot import process_message, update_conversation_log, generate_response, knowledge_log_string_with_keys, knowledge_log_string_without_keys
from Memory import memory_algorithm, generate_summary, format_summary_prompt
from discord import Message
from pprint import pprint


async def handle_message(message, conversation_log, knowledge_log):
    if message.author.bot:
        return
    # Process incoming message and update conversation_log and knowledge_log
    process_message(message, conversation_log, knowledge_log)
    # Print the conversation_log and knowledge_log
    print("\nConversation log:")
    pprint(conversation_log)
    print("\nKnowledge log:")
    print(knowledge_log_string_with_keys(knowledge_log))
    # Generate response using OpenAI API
    response = generate_response(conversation_log, knowledge_log)
    # Send response to the user if it's not empty
    if response.strip():
        await message.channel.send(response)
    else:
        print("No response sent.")
    # Update conversation_log and knowledge_log based on response
    update_conversation_log(message, response, conversation_log)
    memory_algorithm(conversation_log, knowledge_log)




