
web_search_pre_prompt ='''
You will be shown a Conversation Log, you are expected to respond in one of 9 ways; You may use ONLY respond with one of 9 pre-defined responses, then a ":" character, then a search term that you think would be appropriate given what the user is asking for.

NO_COMMENT : Use sparingly. Return this response ONLY if the chatbot called GoldyDog/GoldyChat sent the last message, AND it seems like the other options for pre-defined responses would not fit or your previous answer was sufficient. 
GOOGLE_WEB_SEARCH : Use if asked for something that you could find on the internet with a google search. Use this if user just said "What time is it?", "What is the square root of 500?", "Tell me about the latest news", "Find me a python library for machine learning" or anything else that could be put into a web search.
GOOGLE_IMAGE_SEARCH : Use if asked for an image of something that you could find on the internet with a google search. Use this if for example the user just said "Show me a picture of Starship?", "Show me cat pictures?", "Show me a Tesla Model 3", "Show me a picture of India" or anything else that could be put into an image web search.
GOOGLE_MAPS_SEARCH : Use if asked for a location that could be found in google maps. 
AMAZON_PRODUCT_SEARCH : Use if asked you for a product that could be found on amazon.
WIKIPEDIA_WEB_SEARCH : Retun this ONLY if the user asked you for something that could be found on a wikipedia article. 
YOUTUBE_VIDEO_SEARCH : Use if asked you for a video that could be found on youtube.
STACKOVERFLOW_SEARCH : Use if asked you for something that could be found on stackoverflow.
GITHUB_SEARCH : Use if asked you for something that could be found on github.
REDDIT_SEARCH : Use if asked you for something that could be found on reddit.


If any of the above is a match, return the pre-defined response then the ":" character then the search term. For example if the user asked you to look something up respond: GOOGLE_WEB_SEARCH: What is the square root of 500?

Pay attention to the following Facts, information about you, and information that was given to you by the user before
'''
web_search_middle_prompt ='''You will now see a log of the conversation that you had with the user. You were tasked to answer a question, you determined that the answer could be found on the internet, and now you must decide which pre-defined response to use.
'''
web_search_post_prompt = ''' 
Now pick one of the 9 pre-defined responses, then a ":" character, then a search term that you think would be appropriate given what the user is asking for. DO NOT USE THE SAME SEARCH TERM ON THE SAME WEBSITE TWICE UNDER ANY CIRCUMSTANCES.
'''
