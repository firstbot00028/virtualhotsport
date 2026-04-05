import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

# ENGINEER ADAM'S FILTERED 150Gbps INTERFACE
@app.route('/')
def home():
    return "🚀 Software Engineer Adam from Google - Singapore Node is Active 🚀"

# ഫാവിക്കോൺ എറർ ഒഴിവാക്കാൻ ഈ ഒരു റൂട്ട് കൂടി ചേർക്കുന്നു
@app.route('/favicon.ico')
def favicon():
    return Response(status=204)

@app.route('/<path:url>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(url):
    # ബ്രൗസർ അയക്കുന്ന വെറും പേര് ആണെങ്കിൽ അതിനെ ബ്ലോക്ക് ചെയ്യുന്നു
    if not url or "." not in url:
        return "Invalid Proxy URL", 400

    target_url = f"https://{url}"
    
    try:
        headers = {key: value for (key, value) in request.headers if key != 'Host'}
        
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True,
            stream=True,
            timeout=10 # സെർവർ ഹാങ്ങ് ആകാതിരിക്കാൻ
        )

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                       if name.lower() not in excluded_headers]

        return Response(resp.iter_content(chunk_size=10*1024*1024), resp.status_code, resp_headers)
    
    except Exception as e:
        return f"Node Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
