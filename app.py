from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session handling

# Generate a new math problem
def generate_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-'])

    # Ensure subtraction doesn't result in a negative number
    if operation == '-' and num1 < num2:
        num1, num2 = num2, num1

    correct_answer = num1 + num2 if operation == '+' else num1 - num2
    return num1, operation, num2, correct_answer

@app.route("/", methods=["GET", "POST"])
def math_practice():
    if 'current_problem' not in session:
        session['current_problem'] = generate_problem()
    if 'correct_count' not in session:
        session['correct_count'] = 0
    if 'incorrect_count' not in session:
        session['incorrect_count'] = 0

    message = ""
    message_class = ""
    previous_question = None
    correct_answer = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "quit":
            return redirect(url_for("goodbye"))

        try:
            user_answer = int(request.form["answer"])
            num1, operation, num2, answer = session['current_problem']
            if user_answer == answer:
                message = random.choice([
                    "Great job!", "Well done!", "You're amazing!",
                    "Fantastic work!", "Keep it up!", "You're a math superstar!"
                ])
                message_class = "correct"
                session['correct_count'] += 1
            else:
                message = "Oops! That was incorrect. Keep trying!"
                message_class = "incorrect"
                previous_question = f"{num1} {operation} {num2}"
                correct_answer = answer
                session['incorrect_count'] += 1
        except ValueError:
            message = "Please enter a valid number."
            message_class = "incorrect"

        session['current_problem'] = generate_problem()

    num1, operation, num2, _ = session['current_problem']
    problem = f"{num1} {operation} {num2}"

    return render_template(
        "math_practice.html",
        problem=problem,
        message=message,
        message_class=message_class,
        previous_question=previous_question,
        correct_answer=correct_answer
    )


@app.route("/goodbye")
def goodbye():
    correct_count = session.get('correct_count', 0)
    incorrect_count = session.get('incorrect_count', 0)
    return render_template(
        "goodbye.html",
        correct_count=correct_count,
        incorrect_count=incorrect_count
    )

if __name__ == "__main__":
    app.run(debug=True)
