# AI-Powered Quiz Generator

![alt text](assets/logoheader.png)
This project allows users to create quizzes from YouTube videos using AI-powered transcription and question generation.

## Features

- **User Authentication**: Registration, login, JWT stored in cookies, token refresh, logout.
- **YouTube Integration**: Download audio from videos automatically.
- **Transcription**: Converts audio to text using Whisper.
- **AI Quiz Generation**: Uses Google Gemini to generate exactly 10 multiple-choice questions per video.
- **Quiz Management**: Users can view, update, and delete their quizzes.
- **REST API**: Built with Django REST Framework.

## Installation

```bash
git clone <repository-url>

cd <project-folder>

python -m venv env

source env/bin/activate  # Linux / macOS
       env/Scripts/activate     # Windows
pip install -r requirements.txt

```

## Installation
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver
```
## Use the API endpoints

| Endpoint              | Method           | Description                        |
| --------------------- | ---------------- | ---------------------------------- |
| `/api/register/`      | POST             | Register new user                  |
| `/api/login/`         | POST             | Login and set JWT cookies          |
| `/api/logout/`        | POST             | Logout user and clear cookies      |
| `/api/token/refresh/` | POST             | Refresh JWT access token           |
| `/api/createQuiz/`    | POST             | Create quiz from YouTube video URL |
| `/api/quizzes/`       | GET              | List all user quizzes              |
| `/api/quizzes/<id>/`  | GET, PUT, DELETE | Retrieve, update, delete a quiz    |

## Projekt Structure
auth_app/
├── api/
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── permissions.py
│   ├── authentication.py
├── models.py
├── admin.py
├── ...
core/
├── settings.py
├── urls.py
├── admins.py
├── ...
quiz_app/
├── api/
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── permissions.py
├── services/
│   ├── youtube.py
│   ├── transcription.py
│   ├── gemini.py
│   └── quiz_creator.py
├── utils.py
├── models.py
├── admin.py
├── ...
