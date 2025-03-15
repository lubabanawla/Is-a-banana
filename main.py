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
            # Convert the frame to HSV color space for color detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Define HSV range for a typical yellow color (tweak as needed)
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            # Count the number of pixels within the yellow range
            yellow_pixels = cv2.countNonZero(mask)
            if yellow_pixels > 500:  # Adjust threshold based on your environment
                print("Yellow object detected!")
            else:
                print("No yellow object detected.")

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield a byte string in the format required for a multipart response
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
