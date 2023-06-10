import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io

def get_wikipedia_summary(page_title):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
        response = requests.get(url)

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

def retrieve_visual_content(page_title):
    try:
        url = f"https://en.wikipedia.org/wiki/{page_title}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            image_tags = soup.find_all("img")
            urls = [img["src"] for img in image_tags]
            return urls
        else:
            return []

    except requests.exceptions.RequestException:
        return []

    except Exception as e:
        return []

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
    max_width = 300
    if image.width > max_width:
        ratio = max_width / float(image.width)
        height = int((float(image.height) * float(ratio)))
        image = image.resize((max_width, height), Image.ANTIALIAS)
    st.image(image)

def main():
    st.title("Wikipedia ChatBot")

    user_input = st.text_input("Enter your query")

    if user_input.lower() == "quit":
        st.write("ChatBot: Goodbye!")
    else:
        summary = get_wikipedia_summary(user_input)
        visual_urls = retrieve_visual_content(user_input)
        st.write("ChatBot:", summary)

        if visual_urls:
            image_url = visual_urls[0]
            image = download_image(image_url)
            if image:
                display_image(image)

if __name__ == '__main__':
    main()
