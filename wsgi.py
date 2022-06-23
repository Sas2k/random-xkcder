from app.app import app
import os
import waitress

if __name__ == "__main__":
	waitress.serve(app, listen='0.0.0.0:5003')