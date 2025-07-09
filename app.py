from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
from utils import *
from PIL import Image
import numpy as np

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return render_template("index.html", students=get_all_students())

@app.route('/add', methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form['name']
        student_id = int(request.form['id'])
        add_student_to_db(student_id, name)

        os.makedirs(f"dataset/{student_id}", exist_ok=True)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
                cv2.imwrite(f"dataset/{student_id}/{count}.jpg", face)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow("Collecting Faces", frame)
            if cv2.waitKey(1) == ord('q') or count >= 100:
                break
        cap.release()
        cv2.destroyAllWindows()
        return redirect(url_for("home"))
    return render_template("add_student.html")

@app.route('/delete/<int:id>')
def confirm_delete(id):
    return render_template("confirm_delete.html", student_id=id)

@app.route('/delete_confirmed/<int:id>')
def delete_student(id):
    delete_student_from_db(id)
    path = f"dataset/{id}"
    if os.path.exists(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        os.rmdir(path)
    return redirect(url_for("home"))

@app.route('/train')
def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = [], []
    for dir_name in os.listdir("dataset"):
        for img_name in os.listdir(f"dataset/{dir_name}"):
            img_path = f"dataset/{dir_name}/{img_name}"
            img = Image.open(img_path).convert("L")
            face_np = np.array(img, 'uint8')
            faces.append(face_np)
            ids.append(int(dir_name))
    recognizer.train(faces, np.array(ids))
    os.makedirs("trainer", exist_ok=True)
    recognizer.save("trainer/trainer.yml")
    return redirect(url_for("home"))

@app.route('/recognize')
def recognize_faces():
    names = {id: name for id, name in get_all_students()}
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/trainer.yml")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            id_, conf = recognizer.predict(face)
            if conf < 70:
                name = names.get(id_, "Unknown")
                mark_attendance(name)
            else:
                name = "Unknown"
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect(url_for("home"))

@app.route('/attendance')
def view_attendance():
    try:
        df = pd.read_csv("attendance.csv")
        records = df.to_dict(orient='records')
    except:
        records = []
    return render_template("view_attendance.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
