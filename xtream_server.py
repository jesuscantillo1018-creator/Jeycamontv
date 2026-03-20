from flask import Flask, Response, request
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "http://user.tvcluboficial.com/"
}

@app.route('/stream/<path:target_url>')
def proxy_stream(target_url):
    url = 'http://' + target_url
    query = request.query_string.decode('utf-8')
    if query:
        url += "?" + query
    
    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=10)
        return Response(
            response.iter_content(chunk_size=8192),
            content_type=response.headers.get('Content-Type', 'video/mp2t'),
            status=response.status_code
        )
    except Exception as e:
        print(f"❌ Error al conectar con {url}: {e}")
        return "Canal no disponible", 404

@app.route('/lista.m3u')
def get_m3u():
    try:
        r = requests.get("https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/global_jeycamon.m3u")
        return Response(r.text.replace('http://', 'http://localhost:8081/stream/').replace('https://', 'http://localhost:8081/stream/'), mimetype='audio/x-mpegurl')
    except:
        return "Error cargando lista", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, threaded=True)
