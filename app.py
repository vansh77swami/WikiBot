import streamlit as st
import requests

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

def main():
    st.title("WikiBot")

    user_input = st.text_input("User Input", key="user_input")

    # Check if Enter key was pressed or Send button was clicked
    enter_pressed = st.button("Send") or (st.session_state.user_input and st.session_state.user_input[-1] == '\n')
    
    if enter_pressed:
        # Remove the newline character from user input
        user_input = st.session_state.user_input.rstrip('\n')
        
        if user_input.lower() == "quit":
            st.write("WikiBot: Goodbye!")
        else:
            summary = get_wikipedia_summary(user_input)
            st.write(f"WikiBot: {summary}")

    # Clear the input field after sending the message
    if enter_pressed:
        st.session_state.user_input = ''

if __name__ == '__main__':
    main()
