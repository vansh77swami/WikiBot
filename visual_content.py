import requests
from bs4 import BeautifulSoup

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
