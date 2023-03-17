#!/usr/bin/env python3
"""App module."""


from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def Bienvenue() -> str:
    """Return welcome message."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
