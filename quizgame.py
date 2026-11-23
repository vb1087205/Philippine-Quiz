import tkinter as tk
from tkinter import messagebox
import random
import os

QUESTIONS = [
    {
        "question": "Who was the first President of the Philippines?",
        "choices": ["A. Manuel L. Quezon", "B. Emilio Aguinaldo", "C. Jose P. Laurel", "D. Ramon Magsaysay"],
        "answer": "B"
    },
    {
        "question": "What is the national flower of the Philippines?",
        "choices": ["A. Rose", "B. Orchid", "C. Sampaguita", "D. Gumamela"],
        "answer": "C"
    },
    {
        "question": "Which is the highest mountain in the Philippines?",
        "choices": ["A. Mount Mayon", "B. Mount Pulag", "C. Mount Apo", "D. Mount Everest"],
        "answer": "C"
    },
    {
        "question": "When is Philippine Independence Day celebrated?",
        "choices": ["A. June 12", "B. August 21", "C. July 4", "D. December 30"],
        "answer": "A"
    },
    {
        "question": "Who wrote the famous novel Noli Me Tangere?",
        "choices": ["A. Andres Bonifacio", "B. Jose Manalo", "C. Apolinario Mabini", "D. Jose Rizal"],
        "answer": "D"
    },
    {
        "question": "What is the largest island in the Philippines?",
        "choices": ["A. Mindanao", "B. Samar", "C. Luzon", "D. Palawan"],
        "answer": "C"
    },
    {
        "question": "Which Philippine city is known as the Summer Capital of the Philippines?",
        "choices": ["A. Tagaytay", "B. Baguio City", "C. Davao City", "D. Cebu City"],
        "answer": "B"
    },
    {
        "question": "What is the national bird of the Philippines?",
        "choices": ["A. Maya", "B. Kingfisher", "C. Philippine Eagle", "D. Uwak"],
        "answer": "C"
    },
    {
        "question": "In which province can you find the famous Banaue Rice Terraces?",
        "choices": ["A. Benguet", "B. Ifugao", "C. Mountain Province", "D. Kalinga"],
        "answer": "B"
    },
    {
        "question": "Which famous festival in Cebu celebrates the Santo Niño?",
        "choices": ["A. Ati-Atihan Festival", "B. Dinagyang Festival", "C. Panagbenga Festival", "D. Sinulog Festival"],
        "answer": "D"
    }
]


TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)


BG_COLOR = "#0A62B4"     
CARD_COLOR = "#6084B4"      
PRIMARY_COLOR = "#133869"  
PRIMARY_DARK = "#000000"
TEXT_COLOR = "#000000"
SECONDARY_COLOR = "#000000"
ACCENT_COLOR = "#E1EDE8"
BORDER_COLOR = "#DCE5E0"
CORRECT_COLOR = "#287A4B"
WRONG_COLOR = "#B94A48"

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_HEADING = ("Segoe UI", 17, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 11, "bold")

root = tk.Tk()
root.title("Philippine Knowledge Quiz")
root.geometry("750x640")
root.configure(bg=BG_COLOR)
root.resizable(False, False)


quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
selected_answer = tk.StringVar()


timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=30, pady=22)


def get_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(new_score):
    if new_score > get_high_score():
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(new_score))
            return True
        except OSError:
            messagebox.showwarning("High Score", "The high score could not be saved.")
    return False


def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()


def get_choice_text(question, letter):
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def make_button(parent, text, command, primary=True, width=15):
    if primary:
        bg_color = PRIMARY_COLOR
        fg_color = "white"
        active_color = PRIMARY_DARK
    else:
        bg_color = ACCENT_COLOR
        fg_color = TEXT_COLOR
        active_color = BORDER_COLOR

    return tk.Button(
        parent,
        text=text,
        font=FONT_BUTTON,
        bg=bg_color,
        fg=fg_color,
        activebackground=active_color,
        activeforeground=fg_color,
        relief="flat",
        bd=0,
        width=width,
        padx=8,
        pady=8,
        cursor="hand2",
        command=command
    )



def show_start_screen():
    clear_screen()

    tk.Label(
        main_frame,
        text="Philippine Knowledge Quiz",
        font=FONT_TITLE,
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    ).pack(pady=(65, 8))

    tk.Label(
        main_frame,
        text="Test how well you know the Philippines!",
        font=FONT_NORMAL,
        bg=BG_COLOR,
        fg=SECONDARY_COLOR
    ).pack(pady=4)

    info_frame = tk.Frame(
        main_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
        padx=28,
        pady=18
    )
    info_frame.pack(pady=25)

    tk.Label(
        info_frame,
        text=f"{len(QUESTIONS)} Questions   |   {TIME_LIMIT} Seconds Each",
        font=FONT_NORMAL,
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=5)

    tk.Label(
        info_frame,
        text=f"High Score: {get_high_score()} / {len(QUESTIONS)}",
        font=FONT_HEADING,
        bg=CARD_COLOR,
        fg=PRIMARY_COLOR
    ).pack(pady=(10, 5))

    tk.Label(
        main_frame,
        text="Select one answer for each question before the timer runs out.",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=SECONDARY_COLOR
    ).pack(pady=5)

    make_button(main_frame, "Start Quiz", start_quiz, primary=True, width=17).pack(pady=18)


# START OR RESTART THE QUIZ
def start_quiz():
    global quiz_questions, current_question, score, wrong_answers

    stop_timer()
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


# QUESTION SCREEN
def show_question():
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons

    stop_timer()
    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT

    question = quiz_questions[current_question]

    # Top section: question number and timer
    top_frame = tk.Frame(main_frame, bg=BG_COLOR)
    top_frame.pack(fill="x", pady=(4, 12))

    tk.Label(
        top_frame,
        text=f"Question {current_question + 1} of {len(quiz_questions)}",
        font=("Segoe UI", 12, "bold"),
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    ).pack(side="left")

    timer_label = tk.Label(
        top_frame,
        text="",
        font=("Segoe UI", 12, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )
    timer_label.pack(side="right")

    tk.Label(
        main_frame,
        text=f"Score: {score}",
        font=FONT_NORMAL,
        bg=BG_COLOR,
        fg=SECONDARY_COLOR
    ).pack(anchor="w", pady=(0, 10))

    # Question area
    question_card = tk.Frame(
        main_frame,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1,
        padx=20,
        pady=18
    )
    question_card.pack(fill="x", pady=5)

    tk.Label(
        question_card,
        text=question["question"],
        font=FONT_HEADING,
        wraplength=620,
        justify="left",
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", pady=(0, 12))

    # Answer choices
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(
            question_card,
            text=choice,
            variable=selected_answer,
            value=letter,
            font=FONT_NORMAL,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            activebackground=CARD_COLOR,
            activeforeground=TEXT_COLOR,
            selectcolor=ACCENT_COLOR,
            anchor="w",
            padx=8,
            pady=5
        )
        button.pack(fill="x", pady=2)
        choice_buttons.append(button)

    feedback_label = tk.Label(
        main_frame,
        text="",
        font=("Segoe UI", 11, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        wraplength=620
    )
    feedback_label.pack(pady=14)

    # Submit and next buttons
    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=8)

    submit_button = make_button(
        button_frame, "Submit Answer", submit_answer, primary=True
    )
    submit_button.pack(side="left", padx=8)

    last_question = current_question == len(quiz_questions) - 1
    next_button = make_button(
        button_frame,
        "See Results" if last_question else "Next Question",
        next_question,
        primary=False
    )
    next_button.config(state="disabled")
    next_button.pack(side="left", padx=8)

    update_timer()


# TIMER FUNCTIONS
def update_timer():
    global time_left, timer_job

    if answered:
        return

    timer_label.config(
        text=f"Time left: {time_left}s",
        fg=WRONG_COLOR if time_left <= 5 else TEXT_COLOR
    )

    if time_left == 0:
        timer_job = None
        time_up()
        return

    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    global timer_job

    if timer_job is not None:
        try:
            root.after_cancel(timer_job)
        except tk.TclError:
            pass
        timer_job = None


# ANSWER CHECKING
def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    global score, answered

    if answered:
        return

    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]

    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct!", fg=CORRECT_COLOR)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"])
        })
        feedback_label.config(
            text="Wrong! Correct answer: " + get_choice_text(question, question["answer"]),
            fg=WRONG_COLOR
        )

    next_button.config(state="normal")


def time_up():
    global answered

    if answered:
        return

    answered = True
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": get_choice_text(question, question["answer"])
    })

    feedback_label.config(
        text="Time is up! Correct answer: " + get_choice_text(question, question["answer"]),
        fg=WRONG_COLOR
    )
    next_button.config(state="normal")


# NEXT QUESTION
def next_question():
    global current_question

    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


# RESULTS SCREEN
def show_results():
    clear_screen()

    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Excellent work!"
    elif percentage >= 70:
        message = "Good job!"
    elif percentage >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."

    tk.Label(
        main_frame,
        text="Quiz Complete!",
        font=FONT_TITLE,
        bg=BG_COLOR,
        fg=PRIMARY_COLOR
    ).pack(pady=(5, 5))

    tk.Label(
        main_frame,
        text=f"Score: {score} / {total}  ({percentage:.0f}%)",
        font=FONT_HEADING,
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=3)

    tk.Label(
        main_frame,
        text=message,
        font=FONT_NORMAL,
        bg=BG_COLOR,
        fg=SECONDARY_COLOR
    ).pack(pady=3)

    record_text = "New high score!" if new_record else f"High Score: {get_high_score()} / {total}"
    tk.Label(
        main_frame,
        text=record_text,
        font=("Segoe UI", 11, "bold"),
        bg=BG_COLOR,
        fg=CORRECT_COLOR
    ).pack(pady=3)

    tk.Label(
        main_frame,
        text="Answer Review (incorrect answers)",
        font=("Segoe UI", 12, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=(8, 5), anchor="w")

    review_frame = tk.Frame(main_frame, bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")

    review_box = tk.Text(
        review_frame,
        height=9,
        wrap="word",
        font=("Segoe UI", 10),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        padx=10,
        pady=8,
        relief="flat",
        yscrollcommand=scrollbar.set
    )
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")

    review_box.config(state="disabled")

    button_frame = tk.Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=12)

    make_button(
        button_frame, "Restart Quiz", restart_quiz, primary=True
    ).pack(side="left", padx=8)

    make_button(
        button_frame, "Exit", on_close, primary=False
    ).pack(side="left", padx=8)



def restart_quiz():
    start_quiz()


def on_close():
    stop_timer()
    root.destroy()


# RUN THE PROGRAM
root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()