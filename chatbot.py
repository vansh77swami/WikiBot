import wikipedia
import visual_content

def get_wikipedia_summary(page_title):
    try:
        page = wikipedia.page(page_title)
        return page.summary
    except wikipedia.exceptions.PageError:
        return "Page not found."
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]  # Get the first 5 options
        return f"Multiple options found: {', '.join(options)}"

def get_visual_content(page_title):
    try:
        urls = visual_content.retrieve_visual_content(page_title)
        return urls
    except Exception as e:
        return str(e)

def chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        else:
            summary = get_wikipedia_summary(user_input)
            visual_urls = get_visual_content(user_input)
            print("ChatBot:", summary)

            for url in visual_urls:
                print(url)

chat()
