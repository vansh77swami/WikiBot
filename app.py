import requests
import visual_content
from flask import Flask, request

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

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.lower() == "quit":
            return "WikiBot: Goodbye!"
        else:
            summary = get_wikipedia_summary(user_input)
            return f"WikiBot: {summary}"
    else:
        return '''
        <html>
        <head>
            <title>WikiBot</title>
        </head>
        <body>
            <h1>WikiBot</h1>
            <form action="/" method="post">
                <input type="text" name="user_input" placeholder="User Input">
                <input type="submit" value="Send">
            </form>
        </body>
        </html>
        '''

if __name__ == '__main__':
    app.run(debug=True)
