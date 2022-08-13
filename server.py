import os
from src.app import app

if __name__ == "__main__":
    app.url_map.strict_slashes = False

    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")

    app.run(
        host="0.0.0.0",
        debug=DEBUG,
        port=5000,
    )
