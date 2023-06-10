import streamlit as st
import subprocess
import chatbot_logic

def main():
    st.title("ChatBot")
    user_input = st.text_input("User Input")

    if st.button("Submit"):
        if user_input.lower() == "quit":
            st.write("ChatBot: Goodbye!")
        else:
            response = chatbot_logic.get_chatbot_response(user_input)
            st.write("ChatBot: " + response)

if __name__ == '__main__':
    main()
