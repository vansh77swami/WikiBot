import random
import wikipedia

def get_chatbot_response(user_input):
    # Predefined responses
    responses = [
        "Hello!",
        "How can I assist you?",
        "That's interesting.",
        "Tell me more.",
        "I'm sorry, I don't have the answer to that.",
        "Goodbye!"
    ]

    # Process user input and generate a response
    if user_input.lower() == "hello":
        return "Hello, nice to meet you!"
    elif user_input.lower() == "goodbye":
        return "Goodbye, have a great day!"
    elif user_input.lower() == "your name":
        return "I am WikiBot, your knowledgeable assistant!"
    
    else:
        try:
            # Search for user input on Wikipedia
            wikipedia.set_lang("en")  # Set the language of Wikipedia
            page = wikipedia.page(user_input)
            summary = wikipedia.summary(user_input)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation error
            options = e.options[:5]  # Limit the number of options to display
            return f"The term '{user_input}' is ambiguous. Did you mean one of these: {', '.join(options)}?"
        except wikipedia.exceptions.PageError:
            # Handle page not found error
            return "I'm sorry, I couldn't find any information on that topic."
        except Exception as e:
            # Handle other exceptions
            return "I encountered an error while searching for information. Please try again later."

        return random.choice(responses)
