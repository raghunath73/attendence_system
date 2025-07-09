
# 🎓 Face Recognition Attendance System (Flask + OpenCV)

An AI-based attendance system that uses **face recognition** to automatically mark attendance. Built with Flask, OpenCV, and SQLite, this system allows admins to manage students, recognize faces via webcam, and maintain clean attendance logs.

---

## 🚀 Features

- 🧑‍🎓 Add/Delete students from the system
- 📸 Collect 100 face samples per student using webcam
- 🤖 Train the face recognition model (LBPH)
- ✅ Live face recognition and automatic attendance marking
- 📅 Prevents multiple entries for the same student on the same date
- 📁 View all attendance records in a beautiful, Bootstrap-styled web interface
- 🎨 Advanced UI with animations using Bootstrap & CSS
- 🧠 Uses OpenCV's LBPH Face Recognizer
- 💾 Stores data using SQLite and CSV

---

## 🧰 Tech Stack

| Layer          | Technology          |
|----------------|---------------------|
| 🎯 Backend     | Python + Flask      |
| 🎨 Frontend    | HTML, CSS, Bootstrap 5 |
| 📷 Face Recognition | OpenCV (LBPH)    |
| 🧠 Model       | opencv-contrib-python |
| 🗃️ Database    | SQLite (`database.db`) |
| 📈 Attendance Logs | CSV (`attendance.csv`) |

---

## 📁 Folder Structure

```
face-attendance-system/
├── app.py                  # Main Flask app
├── utils.py                # Database and face logic
├── train_model.py          # Trains recognizer (optional CLI version)
├── dataset/                # Collected face images
├── trainer/trainer.yml     # Trained LBPH model
├── templates/              # HTML pages (Jinja2 templates)
│   ├── index.html
│   ├── add_student.html
│   ├── view_attendance.html
│   └── confirm_delete.html
├── static/                 # Custom CSS or images
│   └── style.css
├── attendance.csv          # Attendance log file
├── database.db             # SQLite database
└── requirements.txt        # Required packages
```

---

## 💻 Setup Instructions

### 1. Clone or Download
```bash
git clone https://github.com/your-username/face-attendance-system.git
cd face-attendance-system
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv env
env\Scripts\activate  # Windows
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```python
# Run this once in Python shell or call init_db() in app.py
from utils import init_db
init_db()
```

---

## ▶️ Running the App

```bash
python app.py
```

Open your browser and go to:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 How to Use

1. **Add Student** → Capture face samples using webcam
2. **Train Model** → Train face recognizer on collected images
3. **Mark Attendance** → Recognize faces via webcam, logs to `attendance.csv`
4. **View Attendance** → See who was present and when
5. **Delete Student** → Remove student from database and dataset

---

## 📌 Requirements

```text
Flask
opencv-contrib-python
numpy
pandas
Pillow
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🛠 Future Improvements (Optional)

- 🔐 Admin login with Flask-Login
- 📊 Dashboard with attendance stats
- 🌐 Deploy to PythonAnywhere or Render
- 📤 Export to Excel (`.xlsx`)
- 🔎 Filter by date or student name
- 📱 Mobile responsive UI

---

## 👨‍💻 Author

**A Raghunath Reddy**  
Open to collaborations and improvements! Feel free to fork, clone, or suggest upgrades.

---

## 📜 License

This project is open-source under the MIT License.
