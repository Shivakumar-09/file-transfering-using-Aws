import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from encryption import EncryptionManager
from services.s3_service import S3Service
from services.database_service import DatabaseService
from datetime import datetime
import io

app = Flask(__name__)
app.config.from_object(Config)

@app.template_filter('format_datetime')
def format_datetime_filter(value):
    try:
        # Expected format: 2026-03-04T11:24:14.284452
        dt = datetime.fromisoformat(value)
        return dt.strftime("%B %d, %Y")
    except Exception:
        return value

# Initialize Services
encryption = EncryptionManager()
s3_service = S3Service()
db_service = DatabaseService()

# --- Auth Decorator ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')
            
        hashed_pw = generate_password_hash(password)
        if db_service.create_user(email, hashed_pw, name):
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        else:
            flash("User already exists or database error.", "danger")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db_service.get_user(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = db_service.get_user(session['user'])
    files = db_service.get_user_files(session['user'])
    user_name = user.get('name', 'Scholar') if user else 'Scholar'
    return render_template('dashboard.html', files=files, user_name=user_name)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("No file selected.", "warning")
            return redirect(url_for('upload'))
        
        # 1. Local Encryption (Hybrid Cloud Logic)
        raw_data = file.read()
        encrypted_data = encryption.encrypt_file(raw_data)
        
        # 2. Upload Encrypted Blob to S3
        filename = file.filename
        s3_key = f"{session['user']}/{filename}"
        
        if s3_service.upload_file(io.BytesIO(encrypted_data), s3_key):
            # 3. Store Metadata in DynamoDB
            db_service.store_file_metadata(session['user'], filename, s3_key)
            flash(f"File '{filename}' uploaded and encrypted successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Upload to Cloud failed.", "danger")
            
    return render_template('upload.html')

@app.route('/download/<file_id>')
@login_required
def download(file_id):
    # Verify ownership
    metadata = db_service.get_file_metadata(file_id)
    if not metadata or metadata['owner'] != session['user']:
        flash("Access Denied.", "danger")
        return redirect(url_for('dashboard'))
    
    # 1. Download Encrypted Blob from S3
    encrypted_blob = s3_service.download_file(metadata['s3_key'])
    
    if encrypted_blob:
        try:
            # 2. Local Decryption (Hybrid Cloud Logic)
            decrypted_data = encryption.decrypt_file(encrypted_blob)
            
            # 3. Serve Decrypted File to User
            return send_file(
                io.BytesIO(decrypted_data),
                download_name=metadata['filename'],
                as_attachment=True
            )
        except Exception as e:
            print(f"Decryption Error: {e}")
            flash("Decryption failed. Data might be corrupted.", "danger")
    else:
        flash("Could not retrieve file from Cloud.", "danger")
    
    return redirect(url_for('dashboard'))

@app.route('/delete/<file_id>')
@login_required
def delete(file_id):
    metadata = db_service.get_file_metadata(file_id)
    if metadata and metadata['owner'] == session['user']:
        # Delete from S3 and DynamoDB
        s3_service.delete_file(metadata['s3_key'])
        db_service.delete_file_metadata(file_id)
        flash("File deleted successfully.", "success")
    else:
        flash("Delete failed.", "danger")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
