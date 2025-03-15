from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define color range for banana
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([40, 255, 255])

            # Create mask and apply morphological operations
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=1)

            # Find contours and filter by area/aspect ratio
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            min_area = 300
            banana_contours = []
            for cnt in contours:
                if cv2.contourArea(cnt) > min_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    aspect_ratio = float(w) / h
                    if 0.3 < aspect_ratio < 1.5:
                        banana_contours.append(cnt)
            
            # Draw bounding boxes if any are found
            for contour in banana_contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if banana_contours:
                cv2.putText(frame, "Banana detected!", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                print("Banana detected!")
            else:
                print("No banana detected!")
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
