# UserTerminal.md

## Overview

The UserTerminal.py file is responsible for handling user input in the terminal. This input can be used to direct the bot's actions or to adjust its behavior. Here are the currently supported commands:

1. **EXIT**: This command stops the bot.

2. **SEND [message]**: This command allows you to simulate sending a message from the terminal as if it were a Discord user.

3. **PRINT_KNOWLEDGE**: This command prints the current state of the bot's global knowledge log.

4. **CHANGE_NLCM_CYCLE_TIME [time in seconds]**: This command changes the cycle time of the NLCM (Natural Language Conversation Model) to the specified number of seconds.

5. **PRINT_RESEARCH**: This command prints the current state of the bot's research log for the terminal.

6. **PRINT_CONVERSATION**: This command prints the current state of the bot's conversation log for the last channel it interacted with.

7. **RUN_NLCM**: This command triggers the Natural Language Conversation Model (NLCM) to run.

Additional commands for web browsing functionality (requires a Puppeteer interface):

8. **GO_TO_URL "url"**: This command navigates the bot to the specified URL.

9. **PRINT_CLICKABLE_ELEMENT_TREE**: This command prints a tree of clickable elements on the current webpage.

10. **SEARCH "site" "query"**: This command performs a search on the specified website with the given query.

Please note that all commands are case-sensitive and need to be entered in uppercase. Furthermore, any parameter enclosed in square brackets [] indicates that you should replace this with your own input without the brackets. For example, in the command SEND [message], you should replace [message] with the actual message you want to send, like SEND Hello, World!
