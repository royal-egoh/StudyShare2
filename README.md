# StudyShare

A Django web app for students to upload and discover academic resources — lecture notes, past questions, and audio files — organized by faculty, department, level, and semester.

## Features

- Google OAuth login only (via `django-allauth`) — no manual registration
- Post-login profile completion (faculty, department, level)
- Upload resources with cascading faculty → department → level selects
- File storage via Cloudinary (raw files, images)
- Folder-style browse page (Faculty → Department → Level → Semester → Resources)
- Home feed scoped to the logged-in user's department/level
- User profile pages with upload stats

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL
- **Auth:** django-allauth (Google OAuth)
- **File storage:** Cloudinary (`django-cloudinary-storage`)
- **Frontend:** Django templates, vanilla CSS/JS

## Project Structure

```
StudyShareNO2/
├── studyshare
│   ├── accounts          # User model, Google auth, profile completion
│   │   ├── migrations
│   │   ├── templates     # login.html, register.html
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── posts              # Resource model, upload/browse/detail views
│   │   ├── migrations
│   │   ├── templates     # base.html, home.html, browse.html, upload.html,
│   │   │                 # resource_detail.html, profile.html
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── studyshare          # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── requirements.txt
└── README.md
```

## Setup

**1. Clone and create a virtual environment**
```bash
git clone <repo-url>
cd StudyShareNO2/studyshare
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file** in the `studyshare/` directory (same level as `manage.py`):
```env
DB_NAME=studyshare_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**4. Set up the database**
```bash
python manage.py migrate
```

**5. Run the dev server**
```bash
python manage.py runserver
```

## Google OAuth Setup

In [Google Cloud Console](https://console.cloud.google.com/), under your OAuth client:

- **Authorized JavaScript origins:** `http://127.0.0.1:8000`
- **Authorized redirect URIs:** `http://127.0.0.1:8000/accounts/google/login/callback/`

## Apps

| App | Responsibility |
|---|---|
| `accounts` | Custom user model, Google login, profile completion flow |
| `posts` | Resource model, upload/browse/home/detail views |