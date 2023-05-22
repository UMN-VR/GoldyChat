summarize_link_pre_prompt ='''Pay attention to the following Facts, information about you, and information that was given to you by the user
'''
summarize_link_middle_prompt ='''You will now see a log of the conversation that you had with the user. 
'''

summarize_link_website_prompt ='''You will now see a text representation of the website you must analize 
'''

summarize_link_post_prompt = ''' 
You may respond in one of two ways. Do not respond in a different format under ANY circumstances. 

If there was useful information in the website relating to the conversation with the user please write a short summary of said information.

Othewise respond NO_DATA

'''