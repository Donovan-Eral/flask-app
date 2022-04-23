from src.app import create_app
import sys

sys.path.append("src")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)