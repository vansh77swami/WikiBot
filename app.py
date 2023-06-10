import streamlit as st
import requests
import io
from PIL import Image
import visual_content

# Custom CSS styles
st.markdown("""
<style>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    height: 100%;
    width: 100%;
    font-family: Arial, Helvetica, sans-serif;
}

.logo {
    color: #8e8ea0;
    animation: enlarge-appear 0.4s ease-out;
    stroke: #8e8ea0;
    stroke-width: 2;
}

@keyframes enlarge-appear {
    0% {
        opacity: 0;
        transform: scale(75%) rotate(-90deg);
    }
    to {
        opacity: 1;
        transform: scale(100%) rotate(0deg);
    }
}

.data {
    border-radius: 5px;
    color: #8e8ea0;
    text-align: center;
}

.data:empty {
    display: none;
}

body {
    background-color: #343541;
}

@media (prefers-color-scheme: dark) {
    body {
        background-color: #343541;
    }

    .logo {
        color: #acacbe;
        stroke: #acacbe;
    }
}
</style>
""", unsafe_allow_html=True)

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
    st.image(image, use_column_width=True)

def main():
    st.title("Wikipedia ChatBot")

    # Apply the custom CSS class to the container div
    st.markdown('<div class="container">', unsafe_allow_html=True)

    user_input = st.text_input("User Input")
    if st.button("Send"):
        if user_input.lower() == "quit":
            st.write("ChatBot: Goodbye!")
        else:
            summary = get_wikipedia_summary(user_input)
            visual_urls = get_visual_content(user_input)

            st.markdown('<div class="data">', unsafe_allow_html=True.
