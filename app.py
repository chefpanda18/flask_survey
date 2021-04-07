from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pandaseatbamboo'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def show_survey():
    return render_template('start_survey.html', survey=survey)

@app.route('/start', methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')
    if (len(responses) != qid):
        flash(f"invalid question id: {qid}")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template('questions.html', question_num=qid, question=question)
    

@app.route('/thank_you')
def finished_survey():
    flash('YOURE THE BEST')
    return render_template('/finish_survey.html')

