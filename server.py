from src.app import app

if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", debug=True, port=5000)
