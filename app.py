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
    st.image(image)


def main():
    st.title("Wikipedia ChatBot")

    user_input = st.text_input("Enter a topic")

    if user_input.lower() == "quit":
        st.write("ChatBot: Goodbye!")
    else:
        summary = get_wikipedia_summary(user_input)
        visual_urls = get_visual_content(user_input)

        st.write("ChatBot:", summary)

        if visual_urls:
            image_url = visual_urls[0]  # Assuming the first URL is the desired image
            image = download_image(image_url)
            if image:
                display_image(image)

        st.markdown("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wikipedia ChatBot</title>
            <style>
                /* Add your CSS styles here */
            </style>
        </head>
        <body>
            <!-- Add your HTML content here -->
        </body>
        </html>
        """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
