import hashlib


class SHA256ChecksumMiddleware:
    """
    Přidá X-Checksum-SHA256 (a ETag) z přesně těch bytů,
    které odcházejí klientovi. Musí být ZA GZipMiddleware.
    Netýká se streamingových odpovědí (nemají .content).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)

        # jen odpovědi s materializovaným obsahem
        if hasattr(resp, "content") and resp.content:
            # volitelně omezit na JSON:
            # if (resp.get("Content-Type") or "").split(";")[0].strip().lower() != "application/json":
            #     return resp
            digest = hashlib.sha256(resp.content).hexdigest()
            resp["X-Checksum-SHA256"] = digest
            resp["ETag"] = digest
        return resp