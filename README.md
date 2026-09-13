# StudentVault - Digital Student Portfolio & Certificate Verification

## Quick start
python -m venv venv
venv\\Scripts\\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Open http://127.0.0.1:8000/admin/ to add students, projects and certificates.

## REST API
/api/students/
/api/projects/
/api/certificates/

All are ModelViewSets and support GET, POST, PUT/PATCH and DELETE.

## Docker
Build: docker build -t studentvault .
Run: docker run -p 8000:8000 studentvault

For production, replace SQLite with a managed PostgreSQL database and configure cloud object storage for uploaded certificates.
