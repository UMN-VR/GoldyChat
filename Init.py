#Init.py
from text_colors import Colors
from Actions.NLCM import Init_NLCM
from UserTerminal import Init_terminal_IN
async def Init_Systems():

    Init_Memory_Systems()
    Init_NLPM()
    Init_NLCM()
    Init_Feedback_Algorithm()
    Init_IGN()
    Init_CGM()
    Init_Chatbot()
    Init_Discord_Client()
    await Init_terminal_IN()

    print(F"{Colors.RESET}Init Systems... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

def Init_Memory_Systems():
    print(F"{Colors.WHITE}Init Memory Systems... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

def Init_NLPM():
    print(F"{Colors.WHITE}Init NLPM(Natural Language Processing Module)... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")


def Init_Feedback_Algorithm():
    print(F"{Colors.WHITE}Init Feedback Algorithm... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

def Init_IGN():
    print(F"{Colors.WHITE}Init IGN(Image Generator Module)... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

def Init_CGM():
    print(F"{Colors.WHITE}Init CGM(Code Generator Module))... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

def Init_Chatbot():
    print(F"{Colors.WHITE}Init Chatbot... {Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")

def Init_Discord_Client():
    print(f"{Colors.MAGENTA}Launching Discord client...{Colors.RESET}", end='')

    result = "OK"
    print(F"{Colors.GREEN}{result}{Colors.RESET}")