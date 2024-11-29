from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import g4f
import wikipedia

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('home.html')

@socketio.on('message')
def handle_message(message):
    user_question = message['data']
    try:
        wiki_summary = wikipedia.summary(user_question, sentences=3)
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Based on the following information: {wiki_summary}, answer the question: {user_question}"}],
        )
        emit('response', {'data': response})
    except Exception as e:
        emit('response', {'data': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)