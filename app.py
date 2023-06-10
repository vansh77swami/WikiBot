import streamlit as st
import subprocess


def get_wikipedia_response(user_input):
    if user_input.lower() == "quit":
        return "ChatBot: Goodbye!"
    else:
        output = subprocess.check_output(['python', 'chatbot_gui.py', user_input])
        return output.decode()


def main():
    st.title("Wikipedia ChatBot")

    user_input = st.text_input("User Input")
    if st.button("Send"):
        response = get_wikipedia_response(user_input)
        st.write(response)


if __name__ == "__main__":
    main()
