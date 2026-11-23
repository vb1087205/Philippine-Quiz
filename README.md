## Philippine Quiz

Name Joseph Victor I. Briones
Section: BSINFOTECH SE 3-A
Topic: Philippine Quiz
## Features

:10 multiple-choice questions
:Randomized questions
:15-second timer per question
:Automatic answer checking
:Score and percentage calculation
:Review of incorrect answers
## How To Run

:Install Python.
:Open the project folder in VS Code
:Open the terminal.
## How the Questions Are Stored and Shuffled

I stored the questions in a list of dictionaries. Each question has four choices and one correct answer.
I used random.sample() to shuffle the questions every time the quiz starts.

## How the Timer Works

Each question starts with 15 seconds. I used root.after() to update the timer every second.
When an answer is submitted, the timer stops using root.after_cancel(). 
If time runs out, the question is marked wrong.

## How the Program Identifies 

The program gets the letter selected by the player and compares it with the correct
answer stored in the question. If they match, the score increases by one.

## How the Score and High Score Work

The percentage is calculated by dividing the score by the total number of q
uestions and multiplying the result by 100. The program saves the 
highest score in high_score.txt and 
reads it again when opened.

## Function Explanations


:Purpose
Called When
start_quiz()

:Resets the score and shuffles questions.

Start or Restart is clicked
update_timer()
Updates the countdown.
A question appears
submit_answer()
Checks the selected answer.

:Submit is clicked
save_high_score()
Saves a new highest score.
Results are displayed
show_results()

:Displays the final score and answer review.
All questions are finished
time_up()
Marks the question wrong when time runs out.
Timer reaches zero

## Screenshots
<img width="916" height="825" alt="StartScreen" src="https://github.com/user-attachments/assets/42d8999f-2329-4ecd-9b77-3c42b44773a9" />
<img width="902" height="751" alt="answer feedback" src="https://github.com/user-attachments/assets/daa73d27-bdc7-4683-a62a-9db029adb225" />
<img width="874" height="727" alt="resultss" src="https://github.com/user-attachments/assets/6197666b-d215-499d-9378-c03f207b7180" />


## Challenges I Faced

One of my challenges was choosing the colors and layout for the application. 
I looked at some examples online and
tried different color combinations until I found one that I liked.
