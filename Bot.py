# Bot.py

from pprint import pprint
from Prompts.prompts import instructions_pre_prompt, instructions_prompt, post_prompt
from Actions.NLCM import run_NLCM
from Memory import memory_algorithm, generate_summary, knowledge_log_string_without_keys, knowledge_log_string_with_keys, conversation_log_string
from Feedback import feedbackAlgorithm
from OpenAI import call_openai_api
import re
from Discord import send_discord_message, client, send_discord_message_with_image
from pprint import pprint
from actions import process_action
import asyncio
from OpenAI import call_openai_api
from state import State
from actions import predefined_responses
from actions import process_action
from text_colors import Colors
import time
from run_experiments import run_experiments


#browser = None

async def start_NLCM_timer():
    timer_start = time.time()
    printed_messages = set()  # keep track of which 10-second marks we've already printed a message for
    while True:
        time_passed = time.time() - (State.last_message_time or timer_start)
        if time_passed >= 60:
            # Call the NLCM function here
            print(f"{Colors.BRIGHT_YELLOW}60 seconds have passed. Calling NLCM.{Colors.RESET}")
            State.last_message_time = None
            printed_messages.clear()  # reset the printed_messages set
    
            await run_NLCM()

            timer_start = time.time()
        else:
            ten_seconds_passed = int(time_passed // 10)  # integer division by 10 gives us how many 10-second intervals have passed
            if ten_seconds_passed not in printed_messages:
                print(f"{Colors.WHITE}If no input is given within {60 - int(time_passed)}s, NLCM will be launched.{Colors.RESET}")
                printed_messages.add(ten_seconds_passed)
        await asyncio.sleep(1)  # pause for a second before looping again





def print_loginMSG():
    print(f'\n{Colors.GREEN}Logged in as {Colors.MAGENTA}{client.user}{Colors.GREEN} in "Discord" mode.{Colors.RESET} ', end='')
    
    terminal_access_char    = "✅" if State.terminal_access     else "❌"
    internet_access_char    = "✅" if State.internet_access     else "❌"
    Discord_API_access_char = "✅" if State.Discord_API_access  else "❌"
    debug_char              = "✅" if State.debug_mode          else "❌"
    
    print(f"{Colors.WHITE}Debug:{debug_char}{Colors.RESET}")
    print(f"{Colors.RESET}Connectivity:  {Colors.BRIGHT_YELLOW}Terminal:{terminal_access_char}  {Colors.BLUE}Internet:{internet_access_char}   {Colors.MAGENTA}Discord:{Discord_API_access_char}  {Colors.RESET}")

    print(f"{Colors.RED}WARNING: This bot is in development mode. It is not ready for production. Be Careful if you give it internet Access{Colors.RESET}\n\n")

    print(f'{Colors.BRIGHT_GREEN}GoldyChatAI is ready to receive Discord messages{Colors.RESET}')
 


    # print(f'Send messages to the bot using the "SEND" command.')
    # print(f'Type "EXIT" to exit the terminal.\n{Colors.RESET}')


@client.event
async def on_ready():

    
    print_loginMSG()

    if (State.internet_access):
        print(f"{Colors.BRIGHT_YELLOW}Internet access is enabled. Starting Chrome Browser...{Colors.RESET}")
    

    #await run_experiments()

    client.loop.create_task(start_NLCM_timer())

# Event listener for when a message is received
@client.event
async def on_message(message):

    # Ignore messages from the bot itself
    if message.author.bot:
        #print(f"{Colors.MAGENTA}BOT message{Colors.RESET}\n\n")
        return
    
    print(f"{Colors.MAGENTA}@on_message:{message}{Colors.RESET}")
    State.last_message_time = time.time()
    State.last_channel = message.channel
    State.last_message_author = message.author
    

    
    
    # Get the channel id
    channel_id = message.channel.id
    
    # Initialize user memory if it does not exist
    if channel_id not in State.channel_memory:
        State.channel_memory[channel_id] = {
            'conversation_log': [], 
            'research_log': []
        }
    
    # Get the conversation log for the channel
    channel_conversation_log = State.channel_memory[channel_id]['conversation_log']

    # Get the conversation log for the channel
    research_log = State.channel_memory[channel_id]['research_log']

    # Get server and channel name
    server_name = message.guild.name
    channel = message.channel

    print(f"\n{Colors.MAGENTA}Message from {message.author} in server '{server_name}' and channel '#{channel}': {message.content}{Colors.RESET}")

    await handle_message(server_name, channel, message, channel_conversation_log, State.global_knowledge_log)

#good
async def handle_message(server, channel, message, conversation_log, knowledge_log):
    print("@handle_message:")

    # Ignore messages from the bot itself
    if message.author.bot:
        print(f"{Colors.MAGENTA}BOT message{Colors.RESET}\n\n")
        return

    # Process incoming message and update conversation_log and knowledge_log
    process_message(message, conversation_log, knowledge_log)


    State.response_done = False

    result = ""

    while(not State.response_done):
        print("Generating response...")
        # Generate response using OpenAI API
        response = generate_response(server, channel, conversation_log, knowledge_log)
        #print(f"Response:'{response}'")

        # Handle the response, as part of this you might send multiple messages
        result = await handle_response(server, channel, message, response, conversation_log, knowledge_log, predefined_responses)
        print(f"handle_response result: '{result}'")
        
        if State.response_done:
            break


    if result != "":
        await handle_simple_response(result, channel, conversation_log, knowledge_log)
    print(F"{Colors.GREEN}Done Handling Message{Colors.RESET}\n\n")

    feedbackAlgorithm(result, server, channel, message, conversation_log, knowledge_log)

async def handle_response(server, channel, message, response, conversation_log, knowledge_log, predefined_responses, text=""):
    print(f"@handle_response: '{response}'")

    if State.response_done:
        return "DONE responding!"
    
    # Use a lambda function to delay the import of process_action
    #process_action = lambda action, server, channel, conversation_log, knowledge_log, predefined_responses, text: __import__("actions").process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text)
    #response = await process_action(action, server, channel, conversation_log, knowledge_log, predefined_responses, text)

    # Split response into two parts: action and message_text
    action, _, message_text = response.partition(':')
    if ':' in response:
        print(f"Detected Complex response: '{message_text}' & execute {action} ")

        if action == "GoldyChat:":
            # if used username in response
            # Send response to the user if it's not empty
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)
        
        else:
            await handle_simple_response(message_text, channel, conversation_log, knowledge_log)

            print(f"Running: {action}")
            # Call the corresponding function for the action
            action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)
            return action_result
        

    elif action in predefined_responses:
         # Call the corresponding function for the action
        action_result = await process_action(action.strip(), server, channel, conversation_log, knowledge_log, predefined_responses, text)
        return action_result
    
    else:
        State.response_done = True
        # Send response to the user if it's not empty
        await handle_simple_response(response, channel, conversation_log, knowledge_log)
        return "DONE responding!"










def create_links_summary(links):
    summaries = []
    for link in links:
        text = link.title + '\n' + link.url
        prompt = f"Please summarize the following text: {text}"
        response = call_openai_api(prompt, 1500)
        summary = response.strip()
        summaries.append(summary)
    return summaries










def process_message(message, conversation_log, knowledge_log):
    # Update conversation_log and knowledge_log with the new message
    conversation_log.append({"name": message.author.name, "content": message.content})

def update_conversation_log(response, conversation_log):
    conversation_log.append({"name": "GoldyChat", "content": response})









#good
def generate_response(server, channel, conversation_log, knowledge_log):
    # Format conversation_log and knowledge_log as the OpenAI API prompt
    prompt = instructions_pre_prompt + format_prompt(server, channel, conversation_log, knowledge_log)
    print(f"\n{Colors.BLUE}Sending prompt to OpenAI API:\n'\n{prompt}\n'{Colors.RESET}\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 150)
    print(f"{Colors.BRIGHT_BLUE}@generate_response OpenAI API response: {response}\n\n{Colors.RESET}")
    
    return response.strip()



def format_prompt(server, channel, conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    pre_prompt = f"{knowledge_log_str}\nInstructions:{instructions_prompt}\n"
    conversation_history = f"Server:'{server}'  Channel:'#{channel}\n"
    conversation_history = conversation_history + conversation_log_string(conversation_log) 
    full_prompt = f"{pre_prompt}{conversation_history}{post_prompt} Your response will be analyzed and forwarded to Server:'{server}'  Channel:'#{channel}"
    return full_prompt


async def handle_simple_response(response, channel, conversation_log, knowledge_log):
    if isinstance(response, str):
        await send_discord_message(response, channel)
    elif isinstance(response, list):
        pass
        # for item in response:
        #     if isinstance(item, str):
        #         await send_discord_message(item, message.channel)
        #     else:
        #         await send_discord_message(str(item), message.channel)
    
    #print(f"\nFinal response sent: {response}\n\n")
    # Update conversation_log and knowledge_log based on response
    update_conversation_log(response, conversation_log)
    memory_algorithm(conversation_log, knowledge_log)

