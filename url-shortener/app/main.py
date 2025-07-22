import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, redirect, abort, url_for
from .utils import generate_short_code, is_valid_url
from .models import url_store

app = Flask(__name__)

@app.route('/')
def health_check():
    print("[DEBUG] Health check endpoint called")
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    print("[DEBUG] API health endpoint called")
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    print("[DEBUG] shorten_url called with body:", request.get_data())
    data = request.get_json()
    if not data or 'url' not in data:
        print("[DEBUG] Missing 'url' in request body")
        return jsonify({"error": "Missing 'url' in request body"}), 400

    original_url = data['url']
    print(f"[DEBUG] original_url = {original_url}")
    if not is_valid_url(original_url):
        print(f"[DEBUG] Invalid URL: {original_url}")
        return jsonify({"error": "Invalid URL"}), 400

    # Generate until unique
    code = None
    for i in range(5):
        trial = generate_short_code()
        print(f"[DEBUG] Trial short code #{i+1}: {trial}")
        if url_store.get(trial) is None:
            code = trial
            break
    if code is None:
        print("[DEBUG] Could not generate unique code after 5 attempts")
        return jsonify({"error": "Could not generate unique code"}), 500

    url_store.create(code, original_url)
    print(f"[DEBUG] Stored mapping: {code} -> {original_url}")
    short_url = request.host_url.rstrip('/') + '/' + code
    print(f"[DEBUG] Returning short_url: {short_url}")
    return jsonify({"short_code": code, "short_url": short_url}), 201

@app.route('/<short_code>', methods=['GET', 'POST'])
def redirect_short_url(short_code):
    print(f"[DEBUG] redirect_short_url called for code: {short_code}")
    entry = url_store.get(short_code)
    if not entry:
        print(f"[DEBUG] Code not found: {short_code}")
        # abort(404)
        return jsonify({
            "error": "Not Found",
            "message": f"Resource '{request.path}' not found",
            "status": 404
        }), 404
    url_store.increment_clicks(short_code)
    print(f"[DEBUG] Redirecting to {entry['url']} (clicks now {entry['clicks'] + 1})")
    return redirect(entry["url"], code=302)

@app.route('/api/stats/<short_code>', methods=['GET', 'POST'])
def stats(short_code):
    print(f"[DEBUG] stats called for code: {short_code}")
    entry = url_store.get(short_code)
    if not entry:
        print(f"[DEBUG] Stats: code not found: {short_code}")
        # abort(404)
        return jsonify({
            "error": "Not Found",
            "message": f"Resource '{request.path}' not found",
            "status": 404
        }), 404
    print(f"[DEBUG] Returning stats: {entry}")
    return jsonify({
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"]
    }), 200

if __name__ == '__main__':
    print("[DEBUG] Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)
