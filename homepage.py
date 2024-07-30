import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Set a secret key for the session
app.secret_key = os.urandom(24)

# Route for the index page, renders the homepage
@app.route('/')
def index():
    return render_template('homepage.html')

# Serve static files from the 'static' directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Serve assets from the 'src/assets' directory
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('src/assets', filename)

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
