# tkinter-quiz-system
**Name:** Nash Niño Paul N. Iguiz
**Section:** BS-INFOTECH SE-3A
**Topic:** Software Architecture & Design

## How to Run
1. Install Python (Tkinter comes with it).
2. Download `Quizdevii.py`.
3. Open a terminal in the same folder and run: `python Quizdevii.py`

## Features Completed
- 10 multiple-choice questions
- Random question order
- 15-second countdown timer
- Answer checking and time-out handling
- Score and percentage
- Answer review
- High score saved in a text file
- Restart button

## How the Questions Are Stored and Shuffled
[Write this in your own words.]

## How the Timer Works
[Write this in your own words, including how it stops.]

## How the Program Identifies the Correct Answer
[Write this in your own words.]

## How the Score and High Score Work
[Write this in your own words: the score, the percentage, and how the file is read and saved.]

## Function Explanations
| Function | Purpose | Called when |
|----------|---------|-------------|
| begin_quiz() | Resets the score and shuffles the questions | Start or Play Again is clicked |
| display_question() | Builds the question screen | A new question begins |
| tick_timer() | Shows the time left and counts down every second | A question is displayed |
| confirm_answer() | Checks the answer and updates the score | Submit is clicked |
| handle_timeout() | Marks the question wrong when time runs out | The timer reaches 0 |
| store_best_score() | Writes the score to the text file if it is higher | The results screen is shown |
| display_results() | Shows score, percentage, message, and review | After question 10 |

## Screenshots
![Start screen](screenshots/start.png)
![Question screen](screenshots/question.png)
![Answer feedback](screenshots/feedback.png)
![Results screen](screenshots/results.png)
![High score after reopening](screenshots/high_score.png)

## Challenges I Faced
[What was difficult and how did you solve it?]
