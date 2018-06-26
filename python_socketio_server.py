import socketio
import eventlet
from flask import Flask, render_template
import base64

sio = socketio.Server()
app = Flask(__name__)

def storeImg(newjpgtxt):
	newjpgtxt = newjpgtxt.replace("data:image/jpeg;base64,", "");
	filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
	g = open("out.jpg", "wb")
	g.write(base64.b64decode(newjpgtxt))
	g.close()


@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('text', 'node is talking to python');

@sio.on('image')
def message(sid, data):
    print('message ', data)
    storeImg(data);

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('172.142.28.147', 3000)), app)
