# Deployment des Django PC Webshop APIs auf Render

Diese Dokumentation beschreibt alle notwendigen Schritte und Änderungen, um das Django PC Webshop API erfolgreich auf Render zu deployen.

## Inhaltsverzeichnis
1. [Vorbereitung](#vorbereitung)
2. [Umgebungsvariablen](#umgebungsvariablen)
3. [Anpassungen in der Projektstruktur](#anpassungen-in-der-projektstruktur)
4. [Anpassungen in den Einstellungen](#anpassungen-in-den-einstellungen)
5. [Render-spezifische Dateien](#render-spezifische-dateien)
6. [Deployment auf Render](#deployment-auf-render)
7. [Fehlerbehebung](#fehlerbehebung)

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
PYTHON_PATH=/opt/render/project/src/app
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
cd app
python manage.py collectstatic --no-input
python manage.py migrate
cd ..
```

### Hinzufügen einer Procfile Datei

Erstelle eine `Procfile` Datei im Hauptverzeichnis:

```
web: cd app && gunicorn app.wsgi:application
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

### wsgi.py überprüfen

Stelle sicher, dass `app/app/wsgi.py` den richtigen Pfad für die Einstellungen verwendet:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
```

### manage.py überprüfen

Stelle sicher, dass `app/manage.py` den richtigen Pfad für die Einstellungen verwendet:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
```

### urls.py Pfade überprüfen

Überprüfe in `app/app/urls.py` die Pfade zu den App-URLs und entferne print-Anweisungen:

```python
# App routes
path('', include('app.users.urls')),
path('', include('app.orders.urls')),
path('', include('app.pc_components.urls'))
```

Du kannst die print-Anweisungen entfernen, da sie nur für Debugging-Zwecke gedacht sind.

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
      - key: PYTHON_PATH
        value: "/opt/render/project/src/app"
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

### AttributeError: 'NoneType' object has no attribute 'resolve'

Wenn du die Fehlermeldung `AttributeError: 'NoneType' object has no attribute 'resolve'` erhältst, ist das meistens ein Hinweis auf ein Problem mit den Modulpfaden. Folgende Maßnahmen können helfen:

1. Überprüfe, ob in wsgi.py, settings.py und manage.py konsistente Pfade verwendet werden:
   
   Für app/app/wsgi.py:
   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
   ```
   
   Für app/manage.py:
   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
   ```

2. Prüfe in der Render-Umgebung die korrekte Arbeitspfadstruktur, indem du in den Logs nachschaust, aus welchem Verzeichnis die Anwendung gestartet wird.

3. Stelle sicher, dass der `PYTHONPATH` richtig gesetzt ist, damit Python die Module korrekt finden kann. In der render.yaml wurde hierfür bereits die Umgebungsvariable `PYTHON_PATH=/opt/render/project/src/app` hinzugefügt.

4. Wenn der Fehler weiterhin besteht, füge im Build-Prozess einen Debug-Schritt ein, der die Verzeichnisstruktur und Modulpfade ausgibt:
   ```
   find /opt/render/project/src -type d | sort
   echo $PYTHONPATH
   ```

5. Überprüfe auch, ob es Syntaxfehler in einer deiner URL-Dateien gibt. Manchmal können print-Anweisungen in den URLs-Dateien Probleme verursachen.

### Weitere Debug-Tipps:

1. Setze temporär `DEBUG=True` in den Render-Umgebungsvariablen, um detailliertere Fehlerberichte zu erhalten.

2. Überprüfe die Log-Dateien auf Render für weitere Hinweise auf das Problem.

3. Stelle sicher, dass alle App-Verzeichnisse eine korrekte `__init__.py` Datei enthalten, damit sie als Python-Module erkannt werden.

4. Überprüfe, ob deine Datenbankverbindung funktioniert und die Migrationen erfolgreich ausgeführt werden.

5. Füge einen einfachen URL-Pfad direkt in der app/app/urls.py hinzu, um zu testen, ob grundlegende Routing-Funktionen funktionieren:
   ```python
   from django.http import HttpResponse
   
   def hello_world(request):
       return HttpResponse("Hello, world!")
   
   urlpatterns = [
       # Bestehende URLs...
       path('hello/', hello_world, name='hello_world'),
   ]
   ``` 