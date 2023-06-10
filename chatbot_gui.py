from flask import Flask, render_template, request
import wikipedia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    # Process the user input and generate a response
    response = wikipedia.summary(user_input, sentences=2)
    return response

if __name__ == '__main__':
    app.run(debug=True)
