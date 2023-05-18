# GOOGLE_SEARCH.py File
import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID
from Memory import knowledge_log_string_without_keys, conversation_log_string, get_highest_fact_index, fact_exists
from OpenAI import call_openai_api
from prompts import web_search_pre_prompt, web_search_middle_prompt, web_search_post_prompt
from Link import Link  # Import the Link class

async def search_google(server, channel, conversation_log, knowledge_log, predefined_responses, text=""):
    print("Going into 'search_google' function")
    link_objects = make_google_search(text)

    # Add this loop to summarize each link
    for link in link_objects:
        await link.summarize(channel, conversation_log, knowledge_log)

    return link_objects


def format_answer_web_search_prompt(conversation_log, knowledge_log):
    knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
    full_prompt = f"{web_search_pre_prompt}\n\"{knowledge_log_str}\n\"\n{web_search_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{web_search_post_prompt}"
    return full_prompt

def make_google_search(query):
    print("Going into 'make_google_search' function")
    print("Search query:", query)
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": 5  # Adjust the number of results you want to return
    }
    response = requests.get(url, params=params)
    response_json = response.json()
    
    #print("Google API response:", response_json)

    if "error" in response_json:
        print("Error while searching:", response_json["error"]["message"])
        return "Sorry, I encountered an error while searching."
    results = response_json.get("items", [])
    if not results:
        return []  # Return an empty list
    
    link_objects = []  # List to store Link objects
    for result in results:
        title = result["title"]
        link = result["link"]
        link_object = Link(url=link, title=title)  # Create a Link object
        link_objects.append(link_object)  # Add the Link object to the list

    print(link_objects)
    return link_objects  # Return the list of Link objects
