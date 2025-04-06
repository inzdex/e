from flask import Flask, request, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')

    if not target_url:
        return "Missing 'url' parameter.", 400
    if not target_url.startswith("http"):
        return "Invalid URL. Must start with http or https.", 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Proxy Bot)'
        }
        resp = requests.get(target_url, headers=headers)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Error fetching site: {e}", 500

if __name__ == '__main__':
    app.run(port=8080)
