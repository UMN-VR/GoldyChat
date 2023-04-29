import openai
from config import API_KEY

openai.api_key = API_KEY


def call_openai_api(prompt, max_tokens):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "I'm sorry, I'm having trouble processing your request. Please try again later."

