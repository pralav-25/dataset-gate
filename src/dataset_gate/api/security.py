"""Local API defenses: bounded request bodies, optional bearer tokens and safe headers."""

import hmac

from starlette.responses import JSONResponse

MAX_REQUEST_BYTES = 6_000_000


class SecurityMiddleware:
    def __init__(self, app, token=None):
        self.app = app
        self.token = token.encode("utf-8") if token else None

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])

        async def reject(status, detail):
            await JSONResponse({"detail": detail}, status_code=status)(scope, receive, send)

        if self.token and scope["path"] != "/health":
            if not hmac.compare_digest(headers.get(b"authorization", b""), b"Bearer " + self.token):
                return await reject(401, "valid bearer token required")
        length = headers.get(b"content-length")
        if length is not None:
            try:
                declared = int(length)
            except ValueError:
                return await reject(400, "invalid content length")
            if declared < 0:
                return await reject(400, "invalid content length")
            if declared > MAX_REQUEST_BYTES:
                return await reject(413, "request exceeds 6 MB")
        if scope["method"] in ("POST", "PUT", "PATCH"):
            if (
                headers.get(b"content-type", b"").split(b";")[0].strip().lower()
                != b"application/json"
            ):
                return await reject(415, "application/json required")
        messages, total = [], 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            total += len(message.get("body", b""))
            if total > MAX_REQUEST_BYTES:
                return await reject(413, "request exceeds 6 MB")
            messages.append(message)
            if not message.get("more_body", False):
                break
        position = 0

        async def replay():
            nonlocal position
            if position < len(messages):
                message = messages[position]
                position += 1
                return message
            return {"type": "http.request", "body": b"", "more_body": False}

        async def safe_send(message):
            if message["type"] == "http.response.start":
                message = {
                    **message,
                    "headers": list(message.get("headers", []))
                    + [
                        (b"x-content-type-options", b"nosniff"),
                        (b"referrer-policy", b"no-referrer"),
                        (b"cache-control", b"no-store"),
                    ],
                }
            await send(message)

        await self.app(scope, replay, safe_send)
