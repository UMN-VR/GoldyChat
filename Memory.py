from pprint import pprint
from OpenAI import call_openai_api

def memory_algorithm(conversation_log, knowledge_log):
    # Implement the memory algorithm here to update conversation_log and knowledge_log
    if len(conversation_log) >= 14:
        print("Executing Memory Algorithm:")
        messages_to_summarize = conversation_log[-4:]
        conversation_log = conversation_log[:-4]
        summary = generate_summary(messages_to_summarize, knowledge_log)
        knowledge_log[f"earlier_info{len(knowledge_log)}"] = summary
        # Print the conversation_log and knowledge_log
        print("\nConversation log:")
        pprint(conversation_log)
        print("\nKnowledge log:")
        pprint(knowledge_log)
        print("\n")


def generate_summary(messages_to_summarize, knowledge_log, format_summary_prompt):
    # Generate a summary of the messages_to_summarize using the OpenAI API
    prompt = format_summary_prompt(messages_to_summarize, knowledge_log)
    
    print("Generated Prompt for Summary:")
    print(prompt)
    
    # Call OpenAI API with the generated prompt
    summary = call_openai_api(prompt, 50)
    
    print("Generated Summary:")
    print(summary.strip())
    
    # Return the generated summary
    return summary.strip()

def format_summary_prompt(messages_to_summarize, knowledge_log):
    # Format messages_to_summarize and knowledge_log as a string for the OpenAI API
    pre_prompt = pre_prompt_start
    print("\nMessages to Summarize:")
    for message in messages_to_summarize:
        print(message)
        pre_prompt += f"{message['name'].capitalize()}: {message['content']} | "
    print("\nKnowledge Log:")
    knowledge_text = ""
    for key, value in knowledge_log.items():
        print(f"{key}: {value}")
        knowledge_text += f"{key}: {value}\n"
    prompt = f"{knowledge_text}\n{pre_prompt}Please summarize the last 4 messages in one short sentence."
    print("\nFinal Prompt:")
    print(prompt)
    return prompt