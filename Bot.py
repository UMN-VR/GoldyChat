# Bot.py

from pprint import pprint
from prompts import instructions_pre_prompt, instructions_prompt, post_prompt
from Memory import memory_algorithm, generate_summary, knowledge_log_string_without_keys, knowledge_log_string_with_keys, conversation_log_string
from OpenAI import call_openai_api
import re
from Discord import send_discord_message
from pprint import pprint
from actions import process_action
import asyncio
from OpenAI import call_openai_api

def create_links_summary(links):
    summaries = []
    for link in links:
        text = link.title + '\n' + link.url
        prompt = f"Please summarize the following text: {text}"
        response = call_openai_api(prompt, 1500)
        summary = response.strip()
        summaries.append(summary)
    return summaries



async def handle_response(server, channel, message, response, conversation_log, knowledge_log, predefined_responses, text=""):
    print("@In handle_response:")
    # Use a lambda function to delay the import of process_action
    process_action = lambda action, server, channel, conversation_log, knowledge_log, predefined_responses, text: __import__("actions").process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
    
    # Split response into two parts: action and message_text
    action, _, message_text = response.partition(':')
    if ':' in response:
        print(f"Detected Complex response: {action}")

        if action == "GoldyChat:":
            # if used username in response
            # Send response to the user if it's not empty
            await handle_simple_response(response, message, conversation_log, knowledge_log)
        
        else:
            print(f"Running: {action}")
            # Call the corresponding function for the action
            action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)
            return action_result
        

    elif action in predefined_responses:
         # Call the corresponding function for the action
        action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)
        return action_result
    
    else:
        # Send response to the user if it's not empty
        await handle_simple_response(response, message, conversation_log, knowledge_log)




#good
async def handle_message(server, channel, message, conversation_log, knowledge_log):
    print("@In handle_message:")
    if message.author.bot:
        return
    # Process incoming message and update conversation_log and knowledge_log
    process_message(message, conversation_log, knowledge_log)
    # Generate response using OpenAI API
    response = generate_response(server, channel, conversation_log, knowledge_log)
    print(f"Response:'{response}'")
    
    # Handle the response, as part of this you might send a second message
    result = await handle_response(server, channel, message, response, conversation_log, knowledge_log, predefined_responses)
    print(f"Result:'{result}'")
    print("Done Handling Message")



def process_message(message, conversation_log, knowledge_log):
    # Update conversation_log and knowledge_log with the new message
    conversation_log.append({"name": message.author.name, "content": message.content})

def update_conversation_log(message, response, conversation_log):
    conversation_log.append({"name": "GoldyChat", "content": response})









#good
def generate_response(server, channel, conversation_log, knowledge_log):
    # Format conversation_log and knowledge_log as the OpenAI API prompt
    prompt = instructions_pre_prompt + format_prompt(server, channel, conversation_log, knowledge_log)
    print(f"\nSending prompt to OpenAI API:\n'\n{prompt}\n'\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 150)
    print(f"OpenAI API response: {response}\n\n")
    
    return response.strip()



def format_prompt(server, channel, conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    pre_prompt = f"{knowledge_log_str}\nInstructions:{instructions_prompt}\n"
    conversation_history = f"Server:'{server}'  Channel:'#{channel}\n"
    conversation_history = conversation_history + conversation_log_string(conversation_log) 
    full_prompt = f"{pre_prompt}{conversation_history}{post_prompt} Your response will be analized and fowarded to Server:'{server}'  Channel:'#{channel}"
    return full_prompt


async def handle_simple_response(response, message, conversation_log, knowledge_log):
    if isinstance(response, str):
        await send_discord_message(response, message.channel)
    elif isinstance(response, list):
        pass
        # for item in response:
        #     if isinstance(item, str):
        #         await send_discord_message(item, message.channel)
        #     else:
        #         await send_discord_message(str(item), message.channel)
    
    #print(f"\nFinal response sent: {response}\n\n")
    # Update conversation_log and knowledge_log based on response
    update_conversation_log(message, response, conversation_log)
    memory_algorithm(conversation_log, knowledge_log)


