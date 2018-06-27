import socketio
import eventlet
from flask import Flask, render_template
import base64

sio = socketio.Server()
app = Flask(__name__)

original_image_name = ''

def storeImg(imagename, newjpgtxt):
    print("storing image", imagename)
    newjpgtxt = newjpgtxt.replace("data:image/jpeg;base64,", "")
    g = open(imagename, "wb")
    g.write(base64.b64decode(newjpgtxt))
    g.close()

def processImg(imgpath):
    with open(imgpath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)
    # sio.emit('text', 'node is talking to python');

@sio.on('original_image_name')
def imageName(sid, data):
    print('imageName ', data)
    global original_image_name 
    original_image_name = data

@sio.on('original_image')
def originImg(sid, data):
    print('message ', data)
    global original_image_name 
    storeImg(original_image_name, data)
    sio.emit('got_image', 'got image')
    sio.emit('processed_image', processImg(original_image_name))


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('172.142.28.147', 3000)), app)