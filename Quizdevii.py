# Quizdevii.py
# Quizdevii - Software Architecture & Design
# Tkinter Quiz System (follows Steps 1-13 of the weekly task)

import tkinter as tk
from tkinter import messagebox
import random
import os

# =====================================================================
# STEP 1 - TOPIC AND QUESTIONS (list of dictionaries)
# Replace these with your own topic and questions if you prefer.
# Do not put numbers like "1." in the question text.
# =====================================================================
QUIZ_BANK = [
    {
        "question": "Which architectural style splits an application into "
                    "presentation, business logic, and data layers?",
        "choices": ["A. Layered architecture", "B. Event-driven architecture",
                    "C. Microkernel architecture", "D. Peer-to-peer architecture"],
        "answer": "A"
    },
    {
        "question": "In the MVC pattern, which component manages the data "
                    "and the business rules?",
        "choices": ["A. View", "B. Controller", "C. Model", "D. Router"],
        "answer": "C"
    },
    {
        "question": "In the SOLID principles, what does the letter S stand for?",
        "choices": ["A. Simple Output Logic", "B. Single Responsibility Principle",
                    "C. Secure Object Layer", "D. Shared Operating Library"],
        "answer": "B"
    },
    {
        "question": "Which style builds an application as many small, "
                    "independent services that talk over a network?",
        "choices": ["A. Monolith", "B. Layered", "C. Client-server",
                    "D. Microservices"],
        "answer": "D"
    },
    {
        "question": "Which diagram language is commonly used to model "
                    "software designs?",
        "choices": ["A. HTML", "B. UML", "C. JSON", "D. CSS"],
        "answer": "B"
    },
    {
        "question": "In a client-server architecture, which side sends "
                    "requests for data or services?",
        "choices": ["A. The client", "B. The server", "C. Only the database",
                    "D. The router"],
        "answer": "A"
    },
    {
        "question": "In an event-driven architecture, what is an event?",
        "choices": ["A. A database table", "B. A user interface screen",
                    "C. A programming language",
                    "D. A notification that something happened"],
        "answer": "D"
    },
    {
        "question": "What does API stand for?",
        "choices": ["A. Applied Program Interface",
                    "B. Automated Process Integration",
                    "C. Application Programming Interface",
                    "D. Advanced Page Index"],
        "answer": "C"
    },
    {
        "question": "In software design, what does \"coupling\" describe?",
        "choices": ["A. How strongly modules depend on each other",
                    "B. How fast the code runs",
                    "C. How many lines a file has",
                    "D. How colorful the interface is"],
        "answer": "A"
    },
    {
        "question": "Why do architects use an iterative approach?",
        "choices": ["A. To avoid documenting the design",
                    "B. To refine the design step by step using feedback",
                    "C. To skip testing",
                    "D. To use only one programming language"],
        "answer": "B"
    }
]

# =====================================================================
# STEP 2 - SETTINGS, COLORS, WINDOW AND QUIZ VARIABLES
# =====================================================================
SECONDS_PER_QUESTION = 15
BEST_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

BG_COLOR = "#312c8f"        # window background (navy)
CARD_COLOR = "#1f3260"      # choice buttons and review box
ACCENT_COLOR = "#fca311"    # titles and main buttons (orange)
SELECT_COLOR = "#3a5fa8"    # selected choice
TEXT_COLOR = "#ffffff"
MUTED_COLOR = "#c5cae9"
CORRECT_COLOR = "#9cba39"
WRONG_COLOR = "#e53935"

# Fonts and sizes (design settings)
TITLE_FONT = "Trebuchet MS"
BODY_FONT = "Verdana"
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 820
TIMER_BAR_WIDTH = WINDOW_WIDTH - 60   # window width minus 30px padding on each side
TIMER_BAR_HEIGHT = 14

root = tk.Tk()
root.title("QUIZDEVII - How Well Do You Know Software Design?")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

shuffled_questions = []      # shuffled copy of the questions
question_index = 0     # index of the current question
points = 0
seconds_left = SECONDS_PER_QUESTION
missed_questions = []       # details of incorrect answers (for the review)
timer_id = None         # id of the scheduled timer, needed to cancel it
question_done = False         # True after the question is submitted

picked_letter = tk.StringVar()   # holds the chosen letter

# Widgets that change while the quiz is running
countdown_label = None
time_bar = None
message_label = None
submit_btn = None
next_btn = None
option_buttons = []

page = tk.Frame(root, bg=BG_COLOR)
page.pack(fill="both", expand=True, padx=30, pady=25)


# =====================================================================
# STEP 3 - HIGH SCORE FUNCTIONS (file handling)
# =====================================================================
def load_best_score():
    """Read the saved high score. Return 0 if there is no valid file."""
    if os.path.exists(BEST_SCORE_FILE):
        try:
            with open(BEST_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def store_best_score(new_score):
    """Save the score only if it beats the old high score."""
    if new_score > load_best_score():
        try:
            with open(BEST_SCORE_FILE, "w") as file:
                file.write(str(new_score))
            return True
        except OSError:
            return False
    return False


# =====================================================================
# STEP 4 - HELPER FUNCTIONS AND START SCREEN
# =====================================================================
def wipe_screen():
    """Remove every widget from the main frame."""
    for widget in page.winfo_children():
        widget.destroy()


def full_choice_text(question, letter):
    """Return the full choice text (for example 'B. def') from a letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def show_home_screen():
    wipe_screen()
    tk.Label(page, text="QUIZDEVII", font=(TITLE_FONT, 40, "bold"),
             bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=(60, 0))
    tk.Label(page, text="How well do you know software design?",
             font=(TITLE_FONT, 15, "italic"), bg=BG_COLOR,
             fg=MUTED_COLOR).pack(pady=(0, 25))

    # Info card
    stats_card = tk.Frame(page, bg=CARD_COLOR, padx=40, pady=18)
    stats_card.pack(pady=10)
    tk.Label(stats_card,
             text=f"{len(QUIZ_BANK)} questions   |   {SECONDS_PER_QUESTION} seconds each",
             font=(BODY_FONT, 12), bg=CARD_COLOR, fg=TEXT_COLOR).pack()
    tk.Label(stats_card,
             text=f"High Score: {load_best_score()} / {len(QUIZ_BANK)}",
             font=(BODY_FONT, 18, "bold"), bg=CARD_COLOR,
             fg=CORRECT_COLOR).pack(pady=(10, 0))

    tk.Button(page, text="START", font=(BODY_FONT, 16, "bold"),
              bg=ACCENT_COLOR, fg="black", width=20, pady=6,
              command=begin_quiz).pack(pady=(25, 8))
    tk.Button(page, text="EXIT", font=(BODY_FONT, 11, "bold"),
              bg=CARD_COLOR, fg=TEXT_COLOR, width=20,
              command=close_app).pack()


# =====================================================================
# STEP 5 - START THE QUIZ AND SHUFFLE THE QUESTIONS
# =====================================================================
def begin_quiz():
    """Reset everything and shuffle the questions."""
    global shuffled_questions, question_index, points, missed_questions
    halt_timer()   # safety: never let an old timer keep running
    shuffled_questions = random.sample(QUIZ_BANK, len(QUIZ_BANK))
    question_index = 0
    points = 0
    missed_questions = []
    display_question()


# =====================================================================
# STEP 6 - DISPLAY A QUESTION WITH ITS PROGRESS
# =====================================================================
def display_question():
    global seconds_left, question_done, countdown_label, time_bar, message_label
    global submit_btn, next_btn, option_buttons

    wipe_screen()
    question_done = False
    picked_letter.set("")
    seconds_left = SECONDS_PER_QUESTION
    question = shuffled_questions[question_index]

    # Header: question number (left), score (center), timer (right)
    header_row = tk.Frame(page, bg=BG_COLOR)
    header_row.pack(fill="x")
    for column in range(3):
        header_row.columnconfigure(column, weight=1)
    tk.Label(header_row,
             text=f"Question {question_index + 1} of {len(shuffled_questions)}",
             font=(BODY_FONT, 13, "bold"), bg=BG_COLOR,
             fg=ACCENT_COLOR).grid(row=0, column=0, sticky="w")
    tk.Label(header_row, text=f"Score: {points}", font=(BODY_FONT, 13),
             bg=BG_COLOR, fg=MUTED_COLOR).grid(row=0, column=1)
    countdown_label = tk.Label(header_row, text="", font=(BODY_FONT, 13, "bold"),
                           bg=BG_COLOR, fg=TEXT_COLOR)
    countdown_label.grid(row=0, column=2, sticky="e")

    # Time bar (shrinks as the time runs out)
    time_bar = tk.Canvas(page, width=TIMER_BAR_WIDTH,
                          height=TIMER_BAR_HEIGHT, bg=CARD_COLOR,
                          highlightthickness=0)
    time_bar.pack(pady=(10, 0))

    # Question text inside a bordered box
    question_card = tk.Frame(page, bg=BG_COLOR,
                            highlightbackground=ACCENT_COLOR,
                            highlightthickness=2)
    question_card.pack(fill="x", pady=22)
    tk.Label(question_card, text=question["question"],
             font=(TITLE_FONT, 17, "bold"), wraplength=700, justify="left",
             bg=BG_COLOR, fg=TEXT_COLOR).pack(padx=15, pady=15, anchor="w")

    # Answer choices (the value of each button is its letter)
    option_buttons = []
    for choice in question["choices"]:
        letter = choice[0]          # "B. def"  ->  "B"
        button = tk.Radiobutton(
            page, text=choice, variable=picked_letter, value=letter,
            indicatoron=0, font=(BODY_FONT, 12), anchor="w", padx=20, pady=9,
            bg=CARD_COLOR, fg=TEXT_COLOR, selectcolor=SELECT_COLOR,
            activebackground=SELECT_COLOR, activeforeground=TEXT_COLOR,
            disabledforeground=TEXT_COLOR)
        button.pack(fill="x", pady=4)
        option_buttons.append(button)

    message_label = tk.Label(page, text="", font=(BODY_FONT, 12, "bold"),
                              bg=BG_COLOR, fg=TEXT_COLOR, wraplength=740)
    message_label.pack(pady=14)

    # Submit (left) and Next (right) share the width equally
    button_frame = tk.Frame(page, bg=BG_COLOR)
    button_frame.pack(fill="x")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    submit_btn = tk.Button(button_frame, text="SUBMIT",
                              font=(BODY_FONT, 13, "bold"), bg=ACCENT_COLOR,
                              fg="black", pady=6, command=confirm_answer)
    submit_btn.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    last_question = question_index == len(shuffled_questions) - 1
    next_btn = tk.Button(button_frame,
                            text="SEE RESULTS" if last_question else "NEXT",
                            font=(BODY_FONT, 13, "bold"), pady=6,
                            state="disabled", command=go_next)
    next_btn.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    tick_timer()


# =====================================================================
# STEP 7 - COUNTDOWN TIMER
# =====================================================================
def redraw_time_bar():
    """Draw the bar that shrinks as seconds_left goes down."""
    time_bar.delete("all")
    width = int(TIMER_BAR_WIDTH * seconds_left / SECONDS_PER_QUESTION)
    color = WRONG_COLOR if seconds_left <= 5 else ACCENT_COLOR
    time_bar.create_rectangle(0, 0, width, TIMER_BAR_HEIGHT, fill=color, width=0)


def tick_timer():
    """Runs once per second until the question is answered or time is up."""
    global seconds_left, timer_id
    if question_done:
        return
    countdown_label.config(text=f"Time left: {seconds_left}s",
                       fg=WRONG_COLOR if seconds_left <= 5 else TEXT_COLOR)
    redraw_time_bar()
    if seconds_left == 0:
        handle_timeout()
        return
    seconds_left -= 1
    timer_id = root.after(1000, tick_timer)


def halt_timer():
    """Cancel the scheduled timer so it stops counting down."""
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None


# =====================================================================
# STEP 8 - CHECK THE ANSWER AND BLOCK DOUBLE SUBMISSION
# =====================================================================
def freeze_choices(correct_letter=None, chosen_letter=None):
    """Disable the choices and color the correct and wrong ones."""
    for button in option_buttons:
        button.config(state="disabled")
        letter = button.cget("value")
        if correct_letter is not None and letter == correct_letter:
            button.config(bg=CORRECT_COLOR, selectcolor=CORRECT_COLOR)
        elif letter == chosen_letter:
            button.config(bg=WRONG_COLOR, selectcolor=WRONG_COLOR)


def confirm_answer():
    global points, question_done
    if question_done:                      # blocks multiple submissions
        return
    choice = picked_letter.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return

    question_done = True
    halt_timer()
    submit_btn.config(state="disabled")

    question = shuffled_questions[question_index]
    freeze_choices(question["answer"], choice)

    if choice == question["answer"]:  # this line checks the answer
        points += 1
        message_label.config(text="Correct! Nice one!", fg=CORRECT_COLOR)
    else:
        missed_questions.append({
            "question": question["question"],
            "your_answer": full_choice_text(question, choice),
            "correct_answer": full_choice_text(question, question["answer"])
        })
        message_label.config(
            text="Not quite. Correct answer: "
                 + full_choice_text(question, question["answer"]),
            fg=WRONG_COLOR)
    next_btn.config(state="normal")


def handle_timeout():
    """Called when the timer reaches zero. The question counts as wrong."""
    global question_done, timer_id
    if question_done:
        return
    question_done = True
    timer_id = None                  # that timer call has already run
    submit_btn.config(state="disabled")

    question = shuffled_questions[question_index]
    freeze_choices(question["answer"], None)
    missed_questions.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": full_choice_text(question, question["answer"])
    })
    message_label.config(
        text="Time's up! Correct answer: "
             + full_choice_text(question, question["answer"]),
        fg=WRONG_COLOR)
    next_btn.config(state="normal")


# =====================================================================
# STEP 9 - MOVE TO THE NEXT QUESTION
# =====================================================================
def go_next():
    global question_index
    question_index += 1
    if question_index < len(shuffled_questions):
        display_question()
    else:
        display_results()


# =====================================================================
# STEP 10 - RESULTS SCREEN
# =====================================================================
def display_results():
    wipe_screen()
    total_questions = len(shuffled_questions)
    percent = (points / total_questions) * 100
    is_new_best = store_best_score(points)

    if percent >= 90:
        message = "Excellent work, architect!"
    elif percent >= 70:
        message = "Good job! Solid foundations."
    elif percent >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."

    tk.Label(page, text="YOUR RESULTS", font=(TITLE_FONT, 30, "bold"),
             bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=(5, 8))

    summary_card = tk.Frame(page, bg=CARD_COLOR, padx=40, pady=14)
    summary_card.pack(fill="x")
    tk.Label(summary_card,
             text=f"Score: {points} / {total_questions}   ({percent:.0f}%)",
             font=(BODY_FONT, 20, "bold"), bg=CARD_COLOR,
             fg=TEXT_COLOR).pack()
    tk.Label(summary_card, text=message, font=(BODY_FONT, 13), bg=CARD_COLOR,
             fg=MUTED_COLOR).pack(pady=3)
    record_text = ("NEW HIGH SCORE!" if is_new_best
                   else f"High Score: {load_best_score()} / {total_questions}")
    tk.Label(summary_card, text=record_text, font=(BODY_FONT, 13, "bold"),
             bg=CARD_COLOR, fg=CORRECT_COLOR).pack(pady=3)

    # =================================================================
    # STEP 11 - ANSWER REVIEW (Text widget with a Scrollbar)
    # =================================================================
    tk.Label(page, text="Review: the ones you missed",
             font=(BODY_FONT, 12, "bold"), bg=BG_COLOR,
             fg=ACCENT_COLOR).pack(pady=(14, 4), anchor="w")

    review_frame = tk.Frame(page, bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_text = tk.Text(review_frame, height=8, wrap="word",
                         font=(BODY_FONT, 10), bg=CARD_COLOR, fg=TEXT_COLOR,
                         yscrollcommand=scrollbar.set)
    review_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_text.yview)
    review_text.tag_config("wrong", foreground="#ff8a80")
    review_text.tag_config("right", foreground="#a5d6a7")

    if not missed_questions:
        review_text.insert("end", "Perfect! You answered every question correctly.")
    else:
        for number, item in enumerate(missed_questions, start=1):
            review_text.insert("end", f"{number}. {item['question']}\n")
            review_text.insert("end", f"   Your answer: {item['your_answer']}\n",
                              "wrong")
            review_text.insert("end", f"   Correct answer: {item['correct_answer']}\n\n",
                              "right")
    review_text.config(state="disabled")   # read-only

    # =================================================================
    # STEP 12 - RESTART AND EXIT BUTTONS
    # =================================================================
    button_frame = tk.Frame(page, bg=BG_COLOR)
    button_frame.pack(fill="x", pady=15)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    tk.Button(button_frame, text="PLAY AGAIN", font=(BODY_FONT, 13, "bold"),
              bg=ACCENT_COLOR, fg="black", pady=6,
              command=play_again).grid(row=0, column=0, sticky="ew", padx=(0, 8))
    tk.Button(button_frame, text="EXIT", font=(BODY_FONT, 13, "bold"),
              bg=CARD_COLOR, fg=TEXT_COLOR, pady=6,
              command=close_app).grid(row=0, column=1, sticky="ew", padx=(8, 0))


def play_again():
    begin_quiz()   # reshuffles the questions and resets the score


def close_app():
    halt_timer()   # cancel the timer before the window is destroyed
    root.destroy()


# =====================================================================
# STEP 12 (continued) - START THE PROGRAM
# =====================================================================
root.protocol("WM_DELETE_WINDOW", close_app)
show_home_screen()
root.mainloop()