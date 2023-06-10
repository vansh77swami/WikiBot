import requests
from PIL import Image
import visual_content
from flask import Flask, render_template, request

app = Flask(__name__)

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

    # Display the image (modify this according to your HTML structure)
    print(f"Display image: {image}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form.get('user_input')

    if user_input.lower() == "quit":
        response = "ChatBot: Goodbye!"
    else:
        # Process user input and generate a response
        summary = get_wikipedia_summary(user_input)
        visual_urls = get_visual_content(user_input)

        # Generate the chatbot response
        response = "ChatBot: " + summary

        if visual_urls:
            # Display the first image
            image_url = visual_urls[0]  # Assuming the first URL is the desired image
            image = download_image(image_url)
            if image:
                display_image(image)

    return response

if __name__ == '__main__':
    app.run()
