import tkinter as tk
from tkinter import ttk, messagebox
import requests
import io
from PIL import Image, ImageTk
import visual_content

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

    # Convert the image to a Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)

    # Create a label widget to display the image
    image_label = tk.Label(root, image=photo)
    image_label.image = photo  # Store a reference to the image to prevent it from being garbage collected
    image_label.pack()

    # Adjust the window size to accommodate the image
    root.geometry(f"{max_width}x300")

def process_input():
    user_input = input_entry.get()
    summary = get_wikipedia_summary(user_input)
    visual_urls = get_visual_content(user_input)

    output_text.config(state="normal")
    output_text.delete("1.0", "end")
    output_text.insert("end", "ChatBot: " + summary + "\n")

    if visual_urls:
        image_url = visual_urls[0]  # Assuming the first URL is the desired image
        image = download_image(image_url)
        if image:
            display_image(image)

    output_text.config(state="disabled")
    input_entry.delete(0, "end")

def quit_app():
    root.quit()

def change_theme(event):
    selected_theme = theme_combobox.get()

    if selected_theme == "Light":
        root.configure(background="#FFFFFF")
        output_text.configure(background="#FFFFFF", fg="#000000")
        input_entry.config(bg="#FFFFFF", fg="#000000")
        send_button.configure(style="Light.TButton")
        quit_button.configure(style="Light.TButton")
    elif selected_theme == "Dark":
        root.configure(background="#333333")
        output_text.configure(background="#333333", fg="#FFFFFF")
        input_entry.config(bg="#555555", fg="#FFFFFF")
        send_button.configure(style="Dark.TButton")
        quit_button.configure(style="Dark.TButton")

# Create the main window
root = tk.Tk()
root.title("Wikipedia ChatBot")
root.geometry("400x300")
root.resizable(False, False)

# Create and configure the output text area
output_text = tk.Text(root, width=40, height=8, state="disabled", font=("Arial", 12), wrap="word")
output_text.pack(padx=10, pady=10)

# Create and configure the input entry
input_entry = tk.Entry(root, font=("Arial", 12))
input_entry.pack(padx=10, pady=(0, 10))
input_entry.bind("<Return>", lambda event: process_input())

# Create and configure the "Send" button
send_button = ttk.Button(root, text="Send", command=process_input)
send_button.pack(padx=10, pady=(0, 10))

# Create and configure the "Quit" button
quit_button = ttk.Button(root, text="Quit", command=quit_app)
quit_button.pack(padx=10, pady=(0, 10))

# Create and configure the theme selection dropdown menu
theme_combobox = ttk.Combobox(root, values=["Light", "Dark"], state="readonly")
theme_combobox.current(0)
theme_combobox.bind("<<ComboboxSelected>>", change_theme)
theme_combobox.pack(padx=10, pady=(0, 10))

# Define the styles for the dark and light buttons
style = ttk.Style()
style.configure("Dark.TButton", background="#555555")
style.configure("Light.TButton", background="#FFFFFF")

# Start the GUI event loop
root.mainloop()
