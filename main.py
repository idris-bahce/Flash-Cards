from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"

to_learn = {}
try:
    words = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words = pandas.read_csv("data/french_words.csv")

to_learn = words.to_dict(orient="records")
random_word = {}

window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)


def flip_card():
    true_button.config(state=DISABLED)
    card.delete("header")
    card.delete("text")
    card.itemconfig(carts_color, image=card_back)
    card.create_text(400, 150, text="English", font=("Ariel", 40, "bold"), tags="header", fill="white")
    card.create_text(400, 263, text=random_word["English"], font=("Ariel", 60, "bold"), tags="text", fill="white")


def next_card():
    global random_word, flip_timer
    true_button.config(state=ACTIVE)
    window.after_cancel(flip_timer)
    card.delete("text")
    card.delete("header")
    random_word = random.choice(to_learn)
    card.create_text(400, 150, text="French", font=("Ariel", 40, "bold"), tags="header", fill="black")
    card.create_text(400, 263, text=random_word["French"], font=("Ariel", 60, "bold"), tags="text", fill="black")
    card.itemconfig(carts_color, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(random_word)
    print(len(to_learn))
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)



flip_timer = window.after(3000, func=flip_card)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
card = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
carts_color = card.create_image(400, 263, image=card_front)
card.grid(row=0, column=0, columnspan=2)
card.create_text(400, 150, text="", font=("Ariel", 40, "italic"), tags="header")
card.create_text(400, 263, text="", font=("Ariel", 60, "bold"), tags="text")

image_true_button = PhotoImage(file="images/right.png")
true_button = Button(image=image_true_button, highlightthickness=0, padx=50, pady=50, command=is_known)
true_button.grid(row=1, column=0)

image_false_button = PhotoImage(file="images/wrong.png")
false_button = Button(image=image_false_button, highlightthickness=0, padx=50, pady=50, command=next_card)
false_button.grid(row=1, column=1)

next_card()

window.mainloop()
