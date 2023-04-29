import openai
from discord import Message
from prompts import pre_prompt_start, reply_post_prompt, post_prompt

def call_openai_api(full_prompt, tokens):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response

def build_pre_prompt(conversation_log):
    pre_prompt = pre_prompt_start
    for message in conversation_log:
        pre_prompt += f"{message['role'].capitalize()}: {message['content']} | "
    return pre_prompt


async def process_message(message, conversation_log):
    print("in process_message")
    print("log")
    print(conversation_log)
    print("")

    response = generate_response(conversation_log)

    if not response:
        response = "I'm sorry, I couldn't generate a response. Please try again."

    conversation_log.append({"role": "bot", "content": response})
    await message.channel.send(response)

def is_message_a_reply(conversation_log):
    print("in is_message_a_reply")
    # print("log")
    # print(conversation_log)

    print("\n")
    pre_prompt = build_pre_prompt(conversation_log)
    full_prompt = pre_prompt + reply_post_prompt
    print(f"Input prompt: {full_prompt} \n")

    response = call_openai_api(full_prompt, 1000)

    is_reply_text = response.choices[0].text.strip().lower()
    is_reply = is_reply_text == "yes" or is_reply_text == "yes." or is_reply_text == "yes!"
    print(f"OpenAI API response for reply check: {is_reply_text}\n \n")

    return is_reply

async def handle_message(message, conversation_log, client):
    if message.author == client.user:
        return

    is_direct_reply = message.reference and message.reference.resolved.author == client.user
    is_mention = message.content.startswith(f'{client.user.mention} ')

    message_text = message.content[len(client.user.mention) + 1:].strip() if is_mention else message.content.strip()

    conversation_log.append({"role": "user", "content": message_text})

    print(f"Is Direct Reply:{is_direct_reply}")
    print(f"Is mention:{is_mention}")
    print(f"Message Text: {message_text} \n \n ")

    if is_direct_reply or is_mention:
        await process_message(message, conversation_log)
    else:
        print("Checking for indirect response")

        is_reply = is_message_a_reply(conversation_log)

        if is_reply:
            await process_message(message, conversation_log)

def generate_response(conversation_log):
    pre_prompt = build_pre_prompt(conversation_log)

    full_prompt = pre_prompt + post_prompt
    print(f"Input prompt: {full_prompt}")

    response = call_openai_api(full_prompt, 1500)

    message = response.choices[0].text.strip()
    print(f"ChatGPT response: {message}")

    return message
