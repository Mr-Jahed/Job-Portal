from flask import Flask, session, redirect, url_for
import os
from jobs.routes import jobs_bp
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = '2918af47fbd52a70'

# Set resume upload folder and create it
app.config['UPLOAD_FOLDER'] = 'static/resumes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(jobs_bp, url_prefix='/')

# Home route: Redirects based on session role
@app.route("/")
def home():
    # Always redirect to login page on root URL
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
