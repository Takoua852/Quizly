![AI Quiz Generator](assets/logoheader.png)

# AI-Powered Quiz Generator

An AI-powered backend application that generates quizzes from YouTube videos by automatically transcribing audio and creating multiple-choice questions using large language models.

---

## Features

* **User Authentication**: Registration, login, logout, JWT-based authentication stored in HTTP-only cookies, token refresh
* **YouTube Integration**: Automatic audio extraction from YouTube videos
* **Transcription**: Audio-to-text conversion using OpenAI Whisper
* **AI Quiz Generation**: Generates exactly 10 multiple-choice questions per video using Google Gemini
* **Quiz Management**: Create, view, update, and delete quizzes
* **REST API**: Built with Django REST Framework

---

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/<your-username>/ai-powered-quiz-generator.git
cd ai-powered-quiz-generator
python -m venv env
```

### Activate virtual environment

```bash
# Linux / macOS
source env/bin/activate

# Windows
env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

This project uses environment variables for configuration. A template is provided.

```bash
cp .env.template .env
```

### Required Variables

```env
DJANGO_SECRET_KEY=
GOOGLE_GENAI_API_KEY=
```

### Frontend / CORS Configuration

If your frontend runs on a different port (e.g. `3000`, `5173`), update the following variable in your `.env` file:

```env
FRONTEND_URLS=http://localhost:3000
```

> Do **not** commit `.env` files.

---

## VS Code Setup (Optional)

If VS Code shows import warnings (e.g. `Import "dotenv" could not be resolved`), ensure the correct Python interpreter is selected:

1. Open the Command Palette (`Ctrl + Shift + P` / `Cmd + Shift + P`)
2. Select **Python: Select Interpreter**
3. Choose:

   * `env/Scripts/python.exe` (Windows)
   * `env/bin/python` (macOS / Linux)
4. Reload the window

---

## Database Setup & Run Server

All migrations are included in the repository.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## API Endpoints

| Endpoint              | Method           | Description                        |
| --------------------- | ---------------- | ---------------------------------- |
| `/api/register/`      | POST             | Register a new user                |
| `/api/login/`         | POST             | Login and set JWT cookies          |
| `/api/logout/`        | POST             | Logout user and clear cookies      |
| `/api/token/refresh/` | POST             | Refresh JWT access token           |
| `/api/createQuiz/`    | POST             | Create quiz from YouTube video URL |
| `/api/quizzes/`       | GET              | List all user quizzes              |
| `/api/quizzes/<id>/`  | GET, PUT, DELETE | Retrieve, update, delete a quiz    |

---

## Project Structure

```text
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

---

## Notes for Contributors

* Do **not** commit `.env` files
* Ensure the virtual environment is activated before running commands
* Initial installation of AI-related dependencies (Torch, Whisper) may take several minutes

---

## License

This project is intended for educational and demonstration purposes.
