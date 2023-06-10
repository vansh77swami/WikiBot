import streamlit as st
from flask import Flask, render_template, request
import subprocess
import chatbot_logic



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    if user_input.lower() == "quit":
        return "ChatBot: Goodbye!"
    else:
        response = chatbot_logic.get_chatbot_response(user_input)
        return "ChatBot: " + response

if __name__ == '__main__':
    app.run()
