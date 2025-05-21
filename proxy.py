import os
import redis
import requests
from flask import Flask, request, Response, render_template, redirect, url_for
from dotenv import load_dotenv
from urllib.parse import unquote

load_dotenv()

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=False
)

DEFAULT_TTL = int(os.getenv("DEFAULT_TTL", 60))

cache_hits = 0
cache_misses = 0

@app.route('/', methods=['GET'])
def proxy():
    global cache_hits, cache_misses

    raw_url = request.args.get('url')
    if not raw_url:
        return "Parâmetro 'url' obrigatório. Ex: /?url=https://example.com", 400

    full_url = unquote(raw_url)

    cached = redis_client.get(full_url)
    if cached:
        cache_hits += 1
        print(f"[CACHE HIT] {full_url}")
        return Response(cached, content_type='application/octet-stream')

    cache_misses += 1
    print(f"[CACHE MISS] {full_url}")

    try:
        etag_key = f"{full_url}:etag"
        etag = redis_client.get(etag_key)

        headers = {}
        if etag:
            headers['If-None-Match'] = etag.decode()

        origin_response = requests.get(full_url, headers=headers)

        if origin_response.status_code == 304:
            cached = redis_client.get(full_url)
            return Response(cached, content_type='application/octet-stream')

        content = origin_response.content
        origin_headers = origin_response.headers

        cache_control = origin_headers.get("Cache-Control", "")
        ttl = DEFAULT_TTL
        if "max-age" in cache_control:
            try:
                ttl = int(cache_control.split("max-age=")[1].split(",")[0])
            except (IndexError, ValueError):
                pass

        redis_client.setex(full_url, ttl, content)
        if 'ETag' in origin_headers:
            redis_client.setex(etag_key, ttl, origin_headers['ETag'])

        return Response(content, content_type=origin_headers.get("Content-Type", "application/octet-stream"))

    except Exception as e:
        return f"Erro ao buscar {full_url}: {str(e)}", 500


@app.route('/status', methods=['GET'])
def status():
    keys = redis_client.keys('*')
    urls = []

    for key in keys:
        key_str = key.decode()
        if key_str.endswith(':etag'):
            continue

        ttl = redis_client.ttl(key)
        urls.append({
            'url': key_str,
            'ttl': ttl
        })

    return render_template(
        "status.html",
        cache_size=len(urls),
        cached_urls=urls,
        cache_hits=cache_hits,
        cache_misses=cache_misses
    )


@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    global cache_hits, cache_misses
    keys = redis_client.keys('*')
    for key in keys:
        redis_client.delete(key)
    cache_hits = 0
    cache_misses = 0
    return redirect(url_for('status'))


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")