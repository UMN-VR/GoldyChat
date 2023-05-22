import requests
from bs4 import BeautifulSoup
from Link import Link

async def further_investigate_link(server, channel, conversation_log, knowledge_log, predefined_responses, text):
    print("Going into 'INVESTIGATE_LINK' function")

    # Extract the URL from the text
    url = extract_url(text)

    # If a URL is found
    if url:
        # Scrape the title of the link
        title = scrape_title(url)

        # Create a Link object
        link = Link(url=url, title=title, origin="user")

        # Add the link to the conversation log
        conversation_log.append({
            "name": "user",
            "content": link
        })

        # Summarize the link's content
        link.summarize(channel, conversation_log, knowledge_log)

        return f"I found something interesting on the web: {link.title} ({link.url})\n\nSummary: {link.summary}"
    else:
        return "I couldn't find a valid URL in your message. Please provide a valid link."

def extract_url(text):
    # A simple way to extract a URL from the text
    words = text.split()
    for word in words:
        if word.startswith("http://") or word.startswith("https://"):
            return word
    return None

def scrape_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text
        return title
    except:
        return "Unknown title"
