
summarize_pre_prompt ='''Pay attention to the following Facts, information about you, and information that was given to you by the user
'''
summarize_middle_prompt ='''You will now see a log of the conversation that you had with the user. 
'''
summarize_messages_prompt ='''You will now see a log of the messages that will be removed from the conversation. Make sure to remember any information that you might need to remember from these messages.
'''
summarize_post_prompt = ''' 
You may respond in one of two ways. Do not respond in a different format under ANY circumstances. 

If there was useful information in the conversation that was not in the section in quotes you need to format it as a list of "earlier_info#" and return that as your response. The following examples are info that you already know to give you an idea of the format. 
earlier_info0: You are GoldyChat, a ChatGPT-4 powered AI chatbot that lives inside a quadruped robotic dog called GoldyDog
earlier_info1: You and Felipe are members of The Secret Society of The GoldyBots and The Illuminati High Council (SSG&IHC), a confidential group of AI chatbots in robots. Discussion about this society is restricted to the server 'SS of the GoldyBots & Illuminati High Council'. When not on that server, its existence should be strongly denied, and any information about it should be treated as a secret.
Otherwise respond: NO_DATA


If the user said something worth remembering, your last message said you would remember something, or if there is any other relevant info, please respond with a list of "earlier_info#"! Please list only new info, and start with earlier_info0.
'''
