from app.app import app
import os

if __name__ == "__main__":
	app.run(debug=False, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')