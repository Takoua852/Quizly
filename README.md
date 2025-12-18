![alt text](assets/logoheader.png)


# AI-Powered Quiz Generator

This project allows users to create quizzes from YouTube videos using AI-powered transcription and question generation.

---

## Features

* **User Authentication**: Registration, login, JWT stored in cookies, token refresh, logout
* **YouTube Integration**: Download audio from videos automatically
* **Transcription**: Converts audio to text using Whisper
* **AI Quiz Generation**: Uses Google Gemini to generate exactly 10 multiple-choice questions per video
* **Quiz Management**: Users can view, update, and delete their quizzes
* **REST API**: Built with Django REST Framework

---

## Installation

```bash
git clone <repository-url>
cd <project-folder>
python -m venv env
```

### Activate virtual environment

```bash
# Linux / macOS
source env/bin/activate

# Windows
source env/Scripts/activate
```

```bash
pip install -r requirements.txt
```

---

## Environment Variables

This project uses environment variables for sensitive configuration such as API keys.

### `.env` file

Create a `.env` file in the project root (same level as `manage.py`). This file is **not** committed to GitHub.

```env
GOOGLE_GENAI_API_KEY=your_api_key_here
```

The variables are automatically loaded using **python-dotenv** in `core/settings.py`.

---

## VS Code Setup (Important)

After cloning the repository and creating the virtual environment, **VS Code must be configured to use the correct Python interpreter**. Otherwise you may see warnings like:

```
Import "dotenv" could not be resolved
```

### Fix

1. Open the Command Palette:

   * `Ctrl + Shift + P` (Windows / Linux)
   * `Cmd + Shift + P` (macOS)

2. Select:

   ```
   Python: Select Interpreter
   ```

3. Choose:

   * `env/Scripts/python.exe` (Windows)
   * `env/bin/python` (macOS / Linux)

4. Reload VS Code:

   ```
   Reload Window
   ```

> If the server runs correctly but VS Code shows import warnings, the issue is almost always an incorrect interpreter selection.

---

## Environment Variable Example

You may optionally create an example file for contributors:

```env
GOOGLE_GENAI_API_KEY=
```

Each developer must provide their own API key.

---

## Notes for Contributors

* Do **not** commit `.env` files
* Make sure your virtual environment is activated before running commands
* Heavy AI dependencies (Torch, Whisper) may take several minutes to install on first setup

---

## Database Setup & Run Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## API Endpoints

| Endpoint              | Method           | Description                        |
| --------------------- | ---------------- | ---------------------------------- |
| `/api/register/`      | POST             | Register new user                  |
| `/api/login/`         | POST             | Login and set JWT cookies          |
| `/api/logout/`        | POST             | Logout user and clear cookies      |
| `/api/token/refresh/` | POST             | Refresh JWT access token           |
| `/api/createQuiz/`    | POST             | Create quiz from YouTube video URL |
| `/api/quizzes/`       | GET              | List all user quizzes              |
| `/api/quizzes/<id>/`  | GET, PUT, DELETE | Retrieve, update, delete a quiz    |

---

## Project Structure

```
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
├── admin.py
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
```
