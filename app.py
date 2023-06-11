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
    st.set_page_config(page_title="WikiBot", page_icon="wikipedia-logo-globe-wikimedia-foundation-png-favpng-9B5MeGD7PRhFGhhMV28ArnFne-removebg-preview.png")

    st.title("WikiBot")

    user_input = st.text_input("User Input")
    if st.button("Send"):
        if user_input.lower() == "quit":
            st.write("WikiBot: Goodbye!")
        else:
            summary = get_wikipedia_summary(user_input)

            st.write(f"WikiBot: {summary}")


if __name__ == '__main__':
    main()
