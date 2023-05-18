# Link.py file
import requests
from bs4 import BeautifulSoup
from OpenAI import call_openai_api
from prompts import summarize_link_pre_prompt, summarize_link_middle_prompt, summarize_link_website_prompt, summarize_link_post_prompt
from Discord import send_discord_message

def summarize_website_string(website_string):
# Only send the equivalent of the first 1500 tokens of text
    if len(website_string) > 1500:
        website_string = website_string[:1500]
    prompt = f"Please summarize the following website:\n\n{website_string}"
    return call_openai_api(prompt, 1500)

class Link:
    def __init__(self, url, title=None, origin=None):
        self.url = url
        self.title = title
        self.origin = origin
        self.summary = None

    def __str__(self):
        return f"{self.title} ({self.url})"



    async def summarize(self, channel, conversation_log, knowledge_log):
        print("@in summarize link")

        # Fetch and process website content as a string for analysis
        website_string = self.fetch_website_content(self.url)
        print("Generated Website String:\n")
        print(website_string)


        summarized_website_string = summarize_website_string(website_string) 
        print("Generated Summary Website String:\n")
        print(summarized_website_string)

        prompt = self.format_summarize_link_prompt(summarized_website_string, conversation_log, knowledge_log)

        print("Generated Prompt for Link Summary:")
        print(prompt)

        # Call OpenAI API with the generated prompt
        summary = call_openai_api(prompt, 1500)

        print("Generated Summary:")
        print(summary.strip())

        # Set the summary attribute of the Link object
        self.summary = summary.strip()

        await send_discord_message(f"{self.title}\n{self.url}\nSummary: {self.summary}", channel)

    def fetch_website_content(self, url):
        website_string = ''
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            website_string = ' '.join(element.get_text(strip=True) for element in text_elements)
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except requests.exceptions.ConnectionError as e:
            print(f'Connection error occurred: {e}')
        except requests.exceptions.Timeout as e:
            print(f'Timeout error occurred: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Error occurred: {e}')
        except Exception as e:
            print(f'Unknown error occurred: {e}')
        return website_string


    def format_summarize_link_prompt(self, website_string, conversation_log, knowledge_log):
        from Memory import knowledge_log_string_without_keys, conversation_log_string
        knowledge_log_str = knowledge_log_string_without_keys(knowledge_log)
        full_prompt = f"{summarize_link_pre_prompt}\n\"{knowledge_log_str}\n\"\n{summarize_link_middle_prompt}\n\n{conversation_log_string(conversation_log)}\n\n{summarize_link_website_prompt}\n\n{website_string}{summarize_link_post_prompt}\n{self.url}"
        return full_prompt
