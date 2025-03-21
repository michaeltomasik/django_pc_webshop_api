#!/usr/bin/env bash
# Debug-Skript für Render-Deployment

echo "============= DEBUG INFORMATIONEN ============="
echo "Aktuelle Verzeichnisstruktur:"
find /opt/render/project/src -type d -not -path "*/\.*" | sort

echo "============= PYTHON PATH ============="
echo $PYTHONPATH

echo "============= UMGEBUNGSVARIABLEN ============="
env | grep -E "DJANGO|PYTHON|RENDER"

echo "============= MODULPFADE ============="
cd app
python -c "import sys; print(sys.path)"

echo "============= WSGI APPLICATION ============="
cd app
python -c "import os; from importlib import import_module; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings'); settings = import_module('app.settings'); print(f'WSGI_APPLICATION: {settings.WSGI_APPLICATION}')"

echo "============= VERFÜGBARE MODULE ============="
cd app
python -c "import pkgutil; print([p[1] for p in pkgutil.iter_modules()])" 