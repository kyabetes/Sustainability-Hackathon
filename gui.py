from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import requests
import openai

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

openai.api_key = 'YOUR API KEY HERE'

def get_sustainability_advice(detected_item):
    base_prompt = ("Provide me one concise paragraph of sustainability or recyclable recommendations for the following item or prompt, "
                   "and make sure to clarify whether or not it is recyclable. If it isn't, then provide some other sustainability recommendations "
                   "and keep it under one paragraph. Here is the prompt: ")
    full_prompt = base_prompt + detected_item
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  
        prompt=full_prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    advice = response.choices[0].text.strip()
    return advice

def on_enter_press(event):
    subscription_key = 'YOUR KEY HERE'
    endpoint = 'YOUR ENDPONT HERE'
    api_url = f'{endpoint}/vision/v3.1/analyze'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/json'}
    params = {'visualFeatures': 'Objects', 'language': 'en'}
    image_url = entry_1.get()
    
    response = requests.post(api_url, params=params, headers=headers, json={'url': image_url})
    advice_text.delete("1.0", "end")  # clear existing text
    
    if response.status_code == 200:
        analysis = response.json()
        detected_objects = [obj['object'] for obj in analysis.get('objects', [])]
        if detected_objects:
            detected_item_text = ', '.join(detected_objects)
            advice = get_sustainability_advice(detected_item_text)
            advice_text.insert("1.0", advice)  # display advice in the Text widget
        else:
            advice_text.insert("1.0", "No objects detected or recognizable.")
    else:
        advice_text.insert("1.0", f"Failed to analyze image: {response.status_code} {response.text}")

window = Tk()
window.geometry("1280x720")
window.configure(bg="#FFFFFF")

window.title("Recycle AI")

try:
    window.iconbitmap('recycle.ico')  
except:
    print("Icon change not supported on this system.")

canvas = Canvas(window, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(window, image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat")
button_1.place(x=0.0, y=0.0, width=1280.0, height=720.0)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(639.5, 165.0, image=entry_image_1)
entry_1 = Entry(window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=('Helvetica', 15))
entry_1.place(x=100.0, y=125.0, width=1079.0, height=78.0)

advice_text = Text(window, bg="#D9D9D9", fg="#000000", wrap="word", bd=0, highlightthickness=0, font=('Helvetica', 16))
advice_text.place(x=100, y=327, width=890, height=308)

entry_1.bind("<Return>", on_enter_press)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(window, image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_2 clicked"), relief="flat")
button_2.place(x=0.0, y=0.0, width=1280.0, height=95.0)

window.resizable(False, False)
window.mainloop()

# by ky :-) (kyan a. lahiri-clements)