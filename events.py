from extensions import socketio
from flask_socketio import emit
from flask import request, session


users = {}

@socketio.on('connect')
def handle_connect():
    print('cilent connect')

@socketio.on('user-join')
def handle_user_join(username):
    print(f'user {username} joined!')
    users[username] = session['customeremail']

@socketio.on('new_message')
def handle_newmessage(message):
    print(f"new message: {message}")
    email = session['customeremail']
    username = None
    for user in users:
        if users[user] == session['customeremail']:
            username = user

    emit(f'Chat',{'message':message,'username':email},broadcast=True)


@socketio.on('staff-join')
def handle_staff_join(email):
    email = session['staffemail']
    print(f'Staff {email} joined the chat!')
    # Additional logic to notify clients that staff has joined or to load chat history

@socketio.on('new_message2')
def handle_new_message(message):
    print(f"New message: {message}")
    email = session['staffemail']
    # Assuming you're emitting to everyone including sender for simplicity
    emit(f'Chat', {'message': message, 'username': email }, broadcast=True)