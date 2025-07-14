# Personalized Learning Platform

An AI-powered online education system that adapts to learners’ preferences, progress, and goals. This platform offers interactive course materials, quizzes, a chatbot for assistance, and real-time progress tracking.

## 📌 Features

- 🧠 **AI Chatbot**: Instant Q&A and personalized study suggestions
- 🎓 **Course Recommendation**: Based on learner’s preferences and progress
- 📹 **Video Lectures**: Unlock quizzes after watching all videos
- 📊 **Admin Dashboard**: Manage courses, track students, view analytics
- 🧪 **Adaptive Quizzes**: Personalized testing experience
- 📱 **Responsive UI**: Accessible from desktop, tablet, and mobile

## ⚙️ Technologies Used

### Frontend
- HTML, CSS, JavaScript

### Backend
- PHP (User/course management)
- Python (Flask Chatbot API)
- MySQLi (Database)

### AI/ML
- Flask
- Pandas (CSV Q&A matching)
- chardet (for encoding detection)

## 🧰 Project Structure

```bash
project-root/
├── chatbot.py              # Flask-based chatbot server
├── templates/
│   └── chat.html           # Chatbot frontend UI
├── static/
│   └── videos/             # Uploaded course videos
├── Admin_dashboard.php     # Admin dashboard
├── Course.php              # Course listing
├── Courses.php             # Course content and quiz trigger
├── Admin_course.php        # Admin course upload
├── Admin_Videos.php        # Admin video upload
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

## 🚀 How to Run the Project

### 1. Start Backend Services
- Launch **XAMPP** or **WAMP** for Apache + MySQL
- Import `course_list` and `login_db` schemas in phpMyAdmin

### 2. Run Flask Chatbot API
```bash
pip install -r requirements.txt
python chatbot.py
```

Make sure the chatbot runs on `http://127.0.0.1:5000`

### 3. Frontend Access
- Place the project folder inside `htdocs` (if using XAMPP)
- Open browser: `http://localhost/Project/Main-Dashboard.php`

## 📷 Screenshots
- Admin & Student Dashboards
- Chatbot with Q&A
- Course selection and progress tracking
- Adaptive Quiz with unlock logic

## 📈 Future Improvements
- Add NLP capabilities to chatbot
- Host Flask API on cloud (Heroku/AWS)
- Integrate push notifications and gamification
- Launch mobile app version (React Native)

## 📚 License
MIT License
