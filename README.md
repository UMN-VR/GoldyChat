

# GoldyChat: A Python-based Discord Chatbot

GoldyChat is a Python-based chatbot designed to interact with users on Discord. Powered by OpenAI's GPT-3, GoldyChat can engage in conversations, answer questions, and perform various tasks based on user inputs.

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [Contributing](#contributing)
- [Future Plans](#future-plans)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Installation and Setup

1. Clone this repository to your local machine.
2. Install the required Python libraries using pip:
    ```
    pip install -r requirements.txt
    ```
3. Set up your OpenAI API key and Discord bot token in a `.env` file in the root directory of the project. The file should look like this:
    ```
    OPENAI_API_KEY=your_openai_api_key
    DISCORD_BOT_TOKEN=your_discord_bot_token
    ```
4. Run the bot using Python:
    ```
    python Bot.py
    ```

## Usage

To start the bot, simply run the `Bot.py` file. Once the bot is running, you can invite it to your Discord server and interact with it using various commands. For example, you can ask the bot questions, request it to perform tasks, or just engage in casual conversation.

## Code Overview

- `Bot.py`: The main file of the chatbot. It listens for messages on Discord and responds to them using the OpenAI GPT-3 model.
- `OpenAI.py`: Contains the function `openai_query`, which generates responses from the GPT-3 model.
- `config.py`: Loads environment variables from a `.env` file. These variables include the bot token and API keys.
- `prompts.py`: Contains a variety of prompts and instructions for the chatbot, guiding its behavior in different situations.

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make your changes in your branch.
4. Submit a pull request.

Please adhere to this project's coding standards and conventions. If you're not sure about something, feel free to ask!

## Future Plans

We're always looking to improve GoldyChat and add new features. Some of our plans for the future include:

- Improved conversation handling
- More advanced tasks and commands
- Integration with other platforms

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or need support with GoldyChat, please contact us at [email@domain.com](mailto:email@domain.com).

## Acknowledgments

We'd like to thank OpenAI for their amazing GPT-3 model, and the Discord.py team for their excellent library.

### ⚠ Parts of this repo were made by GoldyChat through ChatGPT4 ⚠
use with caution 
