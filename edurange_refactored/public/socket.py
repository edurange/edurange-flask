from edurange_refactored.app import socketapp
from random import random
from threading import Thread, Event

thread = Thread()
thread_stop_event = Event()
def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random()*10, 3)
        print(number)
        socketapp.emit('newnumber', {'number': number}, namespace='/socket_test')
        socketapp.sleep(5)

@socketapp.on('connect', namespace='/socket_test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketapp.start_background_task(randomNumberGenerator)


@socketapp.on('disconnect', namespace='/socket_test')
def test_disconnect():
    from edurange_refactored.app import socketapp
    print('Client disconnected')

