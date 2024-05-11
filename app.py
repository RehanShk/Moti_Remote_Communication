from flask import Flask, render_template, request, Response, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)

# Initialize last frame
last_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global last_frame
    
    # Get the image data from the POST request
    frame_data = request.data
    
    # Convert the byte data to a NumPy array
    nparr = np.frombuffer(frame_data, np.uint8)
    
    # Decode the image array using OpenCV
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Store the frame as the last received frame
    last_frame = frame
    
    return "Frame received"

@app.route('/get_last_frame', methods=['GET'])
def get_last_frame():
    global last_frame
    
    # If a frame has been received, return it as a response
    if last_frame is not None:
        # Convert the last frame to JPEG format
        _, jpeg_frame = cv2.imencode('.jpg', last_frame)
        return Response(jpeg_frame.tobytes(), mimetype='image/jpeg')
    else:
        return "No frame received yet"
