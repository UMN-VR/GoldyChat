# responses.py
from Actions.NO_COMMENT import no_comment
from Actions.MAKE_SMALL_TALK import make_small_talk
from Actions.INVENT_STORY import invent_story
from Actions.CONTROL_GOLDYDOG_ROBOT import control_goldydog_robot
from Actions.CREATE_IMAGE import create_image
from Actions.INVESTIGATE_LINK import investigate_link
from Actions.CONTROL_OTHER_ROBOT import control_other_robot
from Actions.MEMORIZE_FACT import memorize_fact
from Actions.ANSWER_QUESTION import answer_question
from Actions.WRITE_CODE import write_code
from Actions.RUN_TERMINAL_TASK import run_terminal_task


from Actions.ANSWER_WEB_SEARCH import answer_web_search

from Actions.AMAZON_PRODUCT_SEARCH import search_amazon
from Actions.WIKIPEDIA_SEARCH import search_wikipedia
from Actions.YOUTUBE_SEARCH import search_youtube
from Actions.STACKOVERFLOW_SEARCH import search_stackoverflow
from Actions.GITHUB_SEARCH import search_github
from Actions.REDDIT_SEARCH import search_reddit
from Actions.GOOGLE_MAPS_SEARCH import search_maps
from Actions.GOOGLE_SEARCH import search_google

predefined_responses = {
    "NO_COMMENT": no_comment,
    "MAKE_SMALL_TALK": make_small_talk,
    "INVENT_STORY": invent_story,
    "CONTROL_GOLDYDOG_ROBOT": control_goldydog_robot,
    "CREATE_IMAGE": create_image,
    "INVESTIGATE_LINK": investigate_link,
    "CONTROL_OTHER_ROBOT": control_other_robot,
    "MEMORIZE_FACT": memorize_fact,
    "ANSWER_QUESTION": answer_question,
    "ANSWER_WEB_SEARCH": answer_web_search,
    "WRITE_CODE": write_code,
    "RUN_TERMINAL_TASK": run_terminal_task,
    "GOOGLE_WEB_SEARCH": search_google, 
    "GOOGLE_IMAGE_SEARCH": search_google, #TODO: Add image search
    "GOOGLE_MAPS_SEARCH": search_maps,
    "AMAZON_PRODUCT_SEARCH": search_amazon,
    "WIKIPEDIA_SEARCH": search_wikipedia,
    "YOUTUBE_SEARCH": search_youtube,
    "STACKOVERFLOW_SEARCH": search_stackoverflow,
    "GITHUB_SEARCH": search_github,
    "REDDIT_SEARCH": search_reddit,

}