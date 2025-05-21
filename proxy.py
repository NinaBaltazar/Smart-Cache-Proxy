import os
import redis
import requests
from flask import Flask, request, Response, render_template, redirect, url_for
from dotenv import load_dotenv

# Contadores de hits e misses
cache_hits = 0
cache_misses = 0

load_dotenv()

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=False
)

DEFAULT_TTL = int(os.getenv("DEFAULT_TTL", 60))

@app.route('/<path:url>', methods=['GET'])
def proxy(url):
    full_url = f"http://{url}"

    cached = redis_client.get(full_url)
    if cached:
        print(f"[CACHE HIT] {full_url}")
        if cached:
            global cache_hits
        cache_hits += 1
        ...
    else:
        global cache_misses
        cache_misses += 1
        ...

        return Response(cached, content_type='application/octet-stream')

    print(f"[CACHE MISS] {full_url}")
    try:
        # Busca ETag salva (se existir)
        etag_key = f"{full_url}:etag"
        etag = redis_client.get(etag_key)

        headers = {}
        if etag:
            headers['If-None-Match'] = etag.decode()

        origin_response = requests.get(full_url, headers=headers)
        
        if origin_response.status_code == 304:
            print(f"[NOT MODIFIED] {full_url}")
            cached = redis_client.get(full_url)
            return Response(cached, content_type='application/octet-stream')

        content = origin_response.content
        headers = origin_response.headers

        # TTL baseado em Cache-Control
        cache_control = headers.get("Cache-Control", "")
        ttl = DEFAULT_TTL
        if "max-age" in cache_control:
            try:
                ttl = int(cache_control.split("max-age=")[1].split(",")[0])
            except (IndexError, ValueError):
                pass

        # Armazena conteúdo + ETag
        redis_client.setex(full_url, ttl, content)
        if 'ETag' in headers:
            redis_client.setex(etag_key, ttl, headers['ETag'])

        return Response(content, content_type=headers.get("Content-Type", "application/octet-stream"))

    except Exception as e:
        return f"Erro ao buscar {full_url}: {str(e)}", 500
    

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    keys = redis_client.keys('*')
    for key in keys:
        redis_client.delete(key)
    global cache_hits, cache_misses
    cache_hits = 0
    cache_misses = 0
    return redirect(url_for('status'))

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


    return render_template("status.html", cache_size=len(urls), cached_urls=urls)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
