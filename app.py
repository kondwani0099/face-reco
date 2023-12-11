#testing the system 

import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def face_recognition():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        coords = []

        # Create coordinates around the face
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            
            # You can add your custom logic to identify the person based on the image in the "img" folder
            # For example, if the image filename contains "Kondwani", you can recognize it as Kondwani.
            img_path = "img/koko.jpg"  # Replace with the path to your image
            if "Kondwani" in img_path:
                pname = "Kondwani"
                cv2.putText(img, pname, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                
            else:
                cv2.putText(img, "Unknown Person", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            

            coords = [x, y, w, h]
        return coords

    def recognize(img, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face")
        return img

    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)  # Open the default camera (you may need to adjust the camera index)

    while True:
        ret, img = cap.read()
        img = recognize(img, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    # Video streaming route.
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def fr_page():
    """Video streaming home page."""
    return render_template('fr_page.html')  # You can create an HTML template for your page



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=5000, debug=True)
    #for server host  to expose ip address
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
