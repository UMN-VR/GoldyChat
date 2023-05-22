#STACKOVERFLOW_SEARCH.py

import requests
from Link import Link  # Import the Link class
from text_colors import Colors

async def search_stackoverflow(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print(f"@search_stackoverflow: {text}")

    # Call the Stack Overflow API
    print(f"Query text: {text}")
    url = 'https://api.stackexchange.com/2.3/search'
    params = {
        'order': 'desc',
        'sort': 'relevance',
        'intitle': text,
        'site': 'stackoverflow',
        'key': '<YOUR_STACK_OVERFLOW_API_KEY>',
    }

    try:
        print(f"{Colors.YELLOW}Making request to Stack Overflow API{Colors.RESET}")
        response = requests.get(url, params=params)

        # Parse the response
        print("Parsing response")
        response_json = response.json()
        print(f"{Colors.BRIGHT_YELLOW}Response JSON: {response_json}{Colors.RESET}")

        link_objects = []  # List to store Link objects
        for item in response_json['items']:
            title = item['title']
            link = item['link']
            origin = f"stackoverflow.com: '{text}'"
            link_object = Link(url=link, title=title, origin=origin)  # Create a Link object
            link_objects.append(link_object)  # Add the Link object to the list

        # Summarize the Link objects
        print("Summarizing Link objects")
        for link_object in link_objects:
            await link_object.summarize(channel, conversation_log, knowledge_log)

        print(f"Returning list of {len(link_objects)} Link objects")
        return link_objects  # Return the list of Link objects

    except Exception as e:
        print(f"Error during Stack Overflow search: {e}")
        return []  # Return an empty list in case of error
