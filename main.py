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
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            banana_detected = False

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:  
                   
                    hull = cv2.convexHull(cnt, returnPoints=False)
                    if hull is not None and len(hull) > 3:
                        try:
                            defects = cv2.convexityDefects(cnt, hull)
                        except cv2.error as e:
                            defects = None

                        if defects is not None:
                            significant_defects = 0
                            for i in range(defects.shape[0]):
                                s, e, f, d = defects[i, 0]
                                if d > 1000:  
                                    significant_defects += 1
                            if significant_defects >= 1:
                                banana_detected = True
                                break

            if banana_detected:
                print("Banana detected!")
            else:
                print("Not a banana!")

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
