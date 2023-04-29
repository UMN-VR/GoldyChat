from pprint import pprint
from prompts import post_prompt, instructions_prompt, smallTalk_pre_prompt, smallTalk_middle_prompt, smallTalk_post_prompt
from Memory import memory_algorithm, generate_summary, format_summary_prompt
from OpenAI import call_openai_api
import re

def process_message(message, conversation_log, knowledge_log):
    # Update conversation_log and knowledge_log with the new message
    conversation_log.append({"name": message.author.name, "content": message.content})

def update_conversation_log(message, response, conversation_log):
    conversation_log.append({"name": "bot", "content": response})

def generate_response(conversation_log, knowledge_log):
    # Format conversation_log and knowledge_log as the OpenAI API prompt
    prompt = format_prompt(conversation_log, knowledge_log)
    print(f"Sending prompt to OpenAI API:\n{prompt}\n\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 150)
    print(f"OpenAI API response: {response}")

    # Check for pre-defined responses
    predefined_responses = {
        "NO_COMMENT": no_comment,
        "MAKE_SMALL_TALK": make_small_talk,
        "INVENT_STORY": invent_story,
        "CONTROL_GOLDYDOG_ROBOT": control_goldydog_robot,
        "CREATE_IMAGE": create_image,
        "WEB_SEARCH": web_search,
        "CONTROL_OTHER_ROBOT": control_other_robot,
    }

    # Search for a pre-defined response in the OpenAI API response
    match = re.search(rf"\b(?:{'|'.join(predefined_responses.keys())})\b", response)
    if match:
        # Get the pre-defined response
        predefined_response = match.group()

        # Extract the text after the pre-defined response
        text_after_predefined_response = response[match.end():].strip()

        # Get the function corresponding to the pre-defined response
        response_func = predefined_responses[predefined_response]

        # Call the function corresponding to the pre-defined response
        predefined_response_result = response_func(conversation_log, knowledge_log)

        # Combine the text after the pre-defined response and the result of the pre-defined response function
        response = f"{text_after_predefined_response}\n\n{predefined_response_result}"
    else:
        print(f"No predefined response found for {response.strip()}")

    print(f"Final response to be sent: {response}")
    return response.strip()


def no_comment(conversation_log, knowledge_log):
    print("Going into 'no_comment' function")
    return ""


def make_small_talk(conversation_log, knowledge_log):
    # Generate a prompt for making small talk
    prompt = "Generate a small talk response."
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    
    # Print the generated prompt and response
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    
    return response.strip()

def make_small_talk(conversation_log, knowledge_log):
    print("Going into 'make_small_talk' function")
    
    # Format conversation_log and knowledge_log as the OpenAI API prompt
    prompt = format_smallTalk_prompt(conversation_log, knowledge_log)
    print(f"Sending prompt to OpenAI API:\n{prompt}\n\n")
    
    # Call OpenAI API with the generated prompt
    response = call_openai_api(prompt, 1500)
    print(f"OpenAI API response: {response}")
    # Return the generated response
    return response.strip()

def format_smallTalk_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string(knowledge_log)
    full_prompt = f"{smallTalk_pre_prompt}\n{knowledge_log_str}\n\n{smallTalk_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{smallTalk_post_prompt}"
    return full_prompt

def knowledge_log_string(knowledge_log):
    facts = [v for k, v in knowledge_log.items() if k.startswith('fact')]
    info_about_you = [v for k, v in knowledge_log.items() if k.startswith('info_about_you')]
    earlier_info = [v for k, v in knowledge_log.items() if k.startswith('earlier_info')]
    formatted_facts = '\n'.join(f'Fact {i}: {fact}' for i, fact in enumerate(facts))
    formatted_info_about_you = '\n'.join(f'Info About You {i}: {info}' for i, info in enumerate(info_about_you))
    formatted_earlier_info = '\n'.join(f'Earlier Info {i}: {info}' for i, info in enumerate(earlier_info))
    return f"{formatted_facts}\n{formatted_info_about_you}\n{formatted_earlier_info}"


def conversation_log_string(conversation_log):
    conversation_history = "| "
    for message in conversation_log:
        conversation_history += f"{message['name'].capitalize()}: {message['content']} | "
    return f"Conversation Log:\n{conversation_history}"


def invent_story(conversation_log, knowledge_log):
    print("Going into 'invent_story' function")
    return "Once upon a time..."


def control_goldydog_robot(conversation_log, knowledge_log):
    print("Going into 'control_goldydog_robot' function")
    return "I'm controlling GoldyDog now..."


def create_image(conversation_log, knowledge_log):
    print("Going into 'create_image' function")
    return "Here's an image I created..."


def web_search(conversation_log, knowledge_log):
    print("Going into 'web_search' function")
    return "I found something interesting on the web..."


def control_other_robot(conversation_log, knowledge_log):
    print("Going into 'control_other_robot' function")
    return "I'm controlling another robot now..."



def format_prompt(conversation_log, knowledge_log):
    facts = knowledge_log.get("fact0", "")
    info_about_you = "\n".join([knowledge_log.get(f"info_about_you{i}", "") for i in range(2)])
    earlier_info = "\n".join([knowledge_log.get(f"earlier_info{i}", "") for i in range(len(knowledge_log) - 3)])
    pre_prompt = f"Facts:\n{facts}\nInfo About You:\n{info_about_you}\nInstructions:{instructions_prompt}\n"
    conversation_history = "| "
    for message in conversation_log:
        conversation_history += f"{message['name'].capitalize()}: {message['content']} | "
    full_prompt = pre_prompt + conversation_history + post_prompt
    return full_prompt


