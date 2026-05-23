"""
Smart Drafting Engine - Web Demo (All-in-One)
Beauty Contest — 26 Mei 2026

Jalankan: python3 run_web.py
Buka: http://localhost:8500
"""

import os
import sys
import json
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import SmartDraftingEngine

# Try AI engine
try:
    os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
    from ai_engine import process_with_ai
    AI_AVAILABLE = True
    os.chdir(os.path.dirname(__file__))
except Exception:
    AI_AVAILABLE = False
    os.chdir(os.path.dirname(__file__))

# Flask app
app = Flask(__name__, static_folder='web')
CORS(app)

engine = SmartDraftingEngine()

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "Smart Drafting Engine", "version": "1.0.0-poc", "ai": AI_AVAILABLE})

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Get API key from request header (sent from frontend)
    api_key = request.headers.get('X-Groq-API-Key', '').strip()

    # Save to temp
    suffix = Path(file.filename).suffix or '.pdf'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # OCR extraction
        result = engine.process_document(tmp_path)

        # AI extraction (use key from frontend)
        if api_key and result.get("raw_text_preview"):
            raw_text = result.get("raw_text_preview", "")
            try:
                from pdf2image import convert_from_path
                from PIL import Image
                file_path = Path(tmp_path)
                if file_path.suffix.lower() == '.pdf':
                    images = convert_from_path(str(file_path), dpi=300)
                    if len(images) > 3:
                        images = images[:3]
                else:
                    images = [Image.open(str(file_path))]
                full_text = ""
                for img in images:
                    full_text += engine.extract_text(img) + "\n"
                ai_result = process_with_ai(full_text, api_key=api_key)
            except Exception as e:
                ai_result = {"ai_enabled": False, "error": str(e)}
            result["ai"] = ai_result
        else:
            result["ai"] = {"ai_enabled": False, "message": "No API key provided. Set key in Settings."}

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp_path)

    return jsonify(result)


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    port = 8500
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  Smart Drafting Engine - Web Demo                      ║
║  Beauty Contest — 26 Mei 2026                           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  🌐 Open in browser: http://localhost:{port}             ║
║                                                          ║
║  AI: {'✅ Enabled (Groq)' if AI_AVAILABLE else '❌ Disabled (set GROQ_API_KEY in .env)'}
║  OCR: Tesseract 5 + OpenCV                              ║
║                                                          ║
║  Press Ctrl+C to stop                                    ║
╚══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False)
