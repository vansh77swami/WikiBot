import streamlit as st
import requests
import io
from PIL import Image
import visual_content

def get_wikipedia_summary(page_title):
    try:
        # Make a request to the Wikipedia API
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data["extract"]
        else:
            return "Page not found."

    except requests.exceptions.RequestException:
        return "An error occurred while fetching data from Wikipedia."

    except KeyError:
        return "An unexpected error occurred."

    except Exception as e:
        return str(e)

def get_web_search_results(query):
    try:
        # Make a request to the Google Search API
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": "AIzaSyAOakIeKXIPgS3LupdGZ91RjZ0GiqAuVXg",
            "cx": "f7687090c04d34826",
            "q": query
        }
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            search_results = [(item["title"], item["link"]) for item in items]
            return search_results
        else:
            return None

    except requests.exceptions.RequestException:
        return "An error occurred while fetching search results."

    except Exception as e:
        return str(e)


def get_visual_content(page_title):
    try:
        urls = visual_content.retrieve_visual_content(page_title)
        return urls
    except Exception as e:
        return str(e)

def download_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            return image
        else:
            return None
    except requests.exceptions.RequestException:
        return None
    except Exception as e:
        return None

def display_image(image):
    # Resize the image if necessary
    max_width = 300
    if image.width > max_width:
        ratio = max_width / float(image.width)
        height = int((float(image.height) * float(ratio)))
        image = image.resize((max_width, height), Image.ANTIALIAS)

    # Display the image
    st.image(image, use_column_width=True)

def main():
    st.title("Wikipedia ChatBot")

    user_input = st.text_input("User Input")
    if st.button("Send"):
        if user_input.lower() == "quit":
            st.write("ChatBot: Goodbye!")
        else:
            # Check if the user's input is a question or a search query
            if user_input.endswith('?'):
                summary = get_wikipedia_summary(user_input)
                st.write(f"ChatBot: {summary}")
            else:
                search_results = get_web_search_results(user_input)
                if search_results:
                    st.write("ChatBot: Here are some search results:")
                    for title, url in search_results:
                        st.write(f"- [{title}]({url})")
                else:
                    st.write("ChatBot: No search results found.")

            visual_urls = get_visual_content(user_input)
            if visual_urls:
                for image_url in visual_urls:
                    image = download_image(image_url)
                    if image:
                        display_image(image)

if __name__ == '__main__':
    main()
