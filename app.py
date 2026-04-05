import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Software Engineer Adam from Google - 150Gbps Node Active 🚀"

@app.route('/<path:url>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(url):
    target_url = f"https://{url}"
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    headers['X-Link-Speed'] = "150Gbps" # വൈഫൈ ഇൻഫോ സ്പീഡ് മെറ്റാഡാറ്റ

    resp = requests.request(
        method=request.method,
        url=target_url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True,
        stream=True
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

    return Response(resp.iter_content(chunk_size=10*1024*1024), resp.status_code, resp_headers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
