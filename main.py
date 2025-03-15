from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # use the default camera

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_brown = np.array([10, 100, 20])
            upper_brown = np.array([20, 255, 200])
            mask = cv2.inRange(hsv, lower_brown, upper_brown)
            brown_pixels = cv2.countNonZero(mask)
            if brown_pixels > 500: 
                print("Brown object detected!")

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Render the HTML page
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Return the response generated along with the specific media type (mime type)
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
