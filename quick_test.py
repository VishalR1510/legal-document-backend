#!/usr/bin/env python3
import sys
import json

try:
    import numpy
    numpy_ok = True
    numpy_ver = numpy.__version__
except:
    numpy_ok = False
    numpy_ver = "Error"

try:
    from app.core.config import settings
    config_ok = True
    api_key_set = bool(settings.GEMINI_API_KEY)
except Exception as e:
    config_ok = False
    api_key_set = False
    
try:
    from main import app
    app_ok = True
    route_count = len(app.routes)
except Exception as e:
    app_ok = False
    route_count = 0

result = {
    "numpy": {"ok": numpy_ok, "version": numpy_ver},
    "config": {"ok": config_ok, "api_key_set": api_key_set},
    "app": {"ok": app_ok, "routes": route_count}
}

print(json.dumps(result, indent=2))
sys.exit(0 if all([numpy_ok, config_ok, app_ok]) else 1)
