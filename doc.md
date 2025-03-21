# Deployment des Django PC Webshop APIs auf Render

Diese Dokumentation beschreibt alle notwendigen Schritte und Änderungen, um das Django PC Webshop API erfolgreich auf Render zu deployen.

## Inhaltsverzeichnis
1. [Vorbereitung](#vorbereitung)
2. [Umgebungsvariablen](#umgebungsvariablen)
3. [Anpassungen in der Projektstruktur](#anpassungen-in-der-projektstruktur)
4. [Anpassungen in den Einstellungen](#anpassungen-in-den-einstellungen)
5. [Render-spezifische Dateien](#render-spezifische-dateien)
6. [Deployment auf Render](#deployment-auf-render)

## Vorbereitung

Vor dem Deployment müssen einige Vorkehrungen getroffen werden:

1. Stelle sicher, dass das Projekt korrekt unter Git-Versionskontrolle steht
2. Erstelle ein Konto auf [Render](https://render.com/)
3. Stelle sicher, dass alle Abhängigkeiten in `requirements.txt` aufgeführt sind

## Umgebungsvariablen

Umgebungsvariablen müssen auf Render in den Projekteinstellungen konfiguriert werden. Die folgenden Variablen sollten angelegt werden:

```
DATABASE_ADMIN_PASSWORD_RENDER=3WWF231BneQ5ryUFc2PE53EFtG3D1cCL
SECRET_KEY=ein_sicherer_schlüssel
DEBUG=False
ALLOWED_HOSTS=*.render.com,deine-app-url.render.com
```

### Änderungen an .gitignore

Die `.gitignore`-Datei sollte aktualisiert werden, um sicherzustellen, dass keine sensiblen Daten im Repository gespeichert werden:

```
.env
__pycache__/
*.pyc
*.pyo
*.pyd
db.sqlite3
.DS_Store
venv/
.idea/
```

## Anpassungen in der Projektstruktur

### Hinzufügen einer build.sh Datei

Erstelle eine `build.sh` Datei im Hauptverzeichnis des Projekts:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python app/manage.py collectstatic --no-input
python app/manage.py migrate
```

### Hinzufügen einer Procfile Datei

Erstelle eine `Procfile` Datei im Hauptverzeichnis:

```
web: gunicorn --chdir app app.wsgi:application
```

## Anpassungen in den Einstellungen

### settings.py anpassen

In `app/app/settings.py` müssen folgende Änderungen vorgenommen werden:

1. Sicherheitseinstellungen aktualisieren:

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = []
allowed_host = os.getenv('ALLOWED_HOSTS', '*')
if allowed_host is not None:
    ALLOWED_HOSTS.extend(allowed_host.split(','))
```

2. Statische Dateien und Media-Einstellungen anpassen:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Zusätzliche Verzeichnisse für statische Dateien
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

3. Middleware für statische Dateien hinzufügen:

```python
MIDDLEWARE = [
    # Bestehende Middleware...
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Neu hinzufügen
    # Restliche bestehende Middleware...
]

# Whitenoise Konfiguration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### wsgi.py korrigieren

In `app/app/wsgi.py` sollte der richtige Pfad für die Einstellungen verwendet werden:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.app.settings')
```

## Render-spezifische Dateien

### render.yaml hinzufügen

Erstelle eine `render.yaml` Datei im Hauptverzeichnis:

```yaml
services:
  - type: web
    name: django-pc-webshop-api
    env: python
    buildCommand: ./build.sh
    startCommand: cd app && gunicorn app.wsgi:application
    envVars:
      - key: DATABASE_ADMIN_PASSWORD_RENDER
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: "*.render.com,django-pc-webshop-api.onrender.com"
    autoDeploy: true
```

## Deployment auf Render

1. Stelle alle Änderungen unter Git-Versionskontrolle
   ```
   git add .
   git commit -m "Anpassungen für Render Deployment"
   ```

2. Verbinde dein Repository mit Render:
   - Öffne das Render Dashboard
   - Wähle "New" und dann "Web Service"
   - Verbinde mit deinem GitHub/GitLab-Repository
   - Wähle "Python" als Umgebung
   - Setze den Build-Befehl auf `./build.sh`
   - Setze den Start-Befehl auf `cd app && gunicorn app.wsgi:application`
   - Füge die notwendigen Umgebungsvariablen hinzu
   - Klicke auf "Create Web Service"

3. Nach dem Deployment-Prozess sollte deine Anwendung unter der URL verfügbar sein, die Render bereitstellt (z.B. `https://django-pc-webshop-api.onrender.com`)

## Fehlerbehebung

- Überprüfe die Logs in der Render-Oberfläche bei Problemen
- Stelle sicher, dass die Datenbank korrekt konfiguriert ist und verbunden werden kann
- Überprüfe, ob `gunicorn` korrekt installiert und in den `requirements.txt` aufgeführt ist
- Überprüfe die Einstellung des `WSGI_APPLICATION` in `settings.py` 