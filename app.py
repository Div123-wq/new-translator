from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import re

app = Flask(__name__)

def translate_text(text):
    """Translate English text to Kannada using deep-translator."""
    try:
        translator = GoogleTranslator(source='en', target='kn')
        result = translator.translate(text)
        return {"success": True, "translation": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

def transliterate_kannada(text):
    """Get romanized/transliteration of Kannada text."""
    try:
        # Translate English to Kannada, also provide a pronunciation hint
        translator = GoogleTranslator(source='en', target='kn')
        result = translator.translate(text)
        return result
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"success": False, "error": "No text provided"}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({"success": False, "error": "Empty text"}), 400

    # Split into sentences for better translation
    result = translate_text(text)
    return jsonify(result)

@app.route('/detect', methods=['POST'])
def detect_language():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"success": False, "error": "No text provided"}), 400
    
    text = data['text'].strip()
    # Simple English character detection
    english_chars = re.findall(r'[a-zA-Z]', text)
    is_english = len(english_chars) > len(text) * 0.3 if text else False
    
    return jsonify({
        "success": True,
        "is_english": is_english,
        "confidence": len(english_chars) / max(len(text), 1)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
