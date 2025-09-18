"""
Portfolio Application Entry Point
Parth Patel - Senior Data Engineer Portfolio
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5899, host='0.0.0.0')