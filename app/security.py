from secrets import compare_digest, token_urlsafe

from flask import abort, request, session


def csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = token_urlsafe(32)
    return session["csrf_token"]


def validate_csrf() -> None:
    token = request.form.get("csrf_token", "")
    expected_token = session.get("csrf_token")
    if not token or not expected_token or not compare_digest(token, expected_token):
        abort(400)
