import os
import sqlite3
import uuid
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database setup
DATABASE = 'cccd.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            id_number TEXT NOT NULL,
            dob TEXT NOT NULL,
            address TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            issue_place TEXT NOT NULL,
            photo_1 TEXT NOT NULL,
            photo_2 TEXT NOT NULL,
            status TEXT DEFAULT 'OK'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
            session['logged_in'] = True
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Đã đăng xuất.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    citizens = conn.execute('SELECT * FROM citizens').fetchall()
    conn.close()
    return render_template('index.html', citizens=citizens)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        fullname = request.form['fullname']
        id_number = request.form['id_number']
        dob = request.form['dob']
        address = request.form['address']
        issue_date = request.form['issue_date']
        issue_place = request.form['issue_place']
        
        # Handle file uploads
        if 'photo_1' not in request.files or 'photo_2' not in request.files:
            flash('Vui lòng tải lên cả 2 ảnh.', 'danger')
            return redirect(request.url)
            
        photo_1 = request.files['photo_1']
        photo_2 = request.files['photo_2']
        
        if photo_1.filename == '' or photo_2.filename == '':
            flash('Vui lòng chọn ảnh.', 'danger')
            return redirect(request.url)
            
        if photo_1 and allowed_file(photo_1.filename) and photo_2 and allowed_file(photo_2.filename):
            # Generate unique filenames
            ext1 = photo_1.filename.rsplit('.', 1)[1].lower()
            ext2 = photo_2.filename.rsplit('.', 1)[1].lower()
            
            filename1 = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext1}"
            filename2 = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext2}"
            
            photo_1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            photo_2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            
            # Save to database
            try:
                conn = get_db_connection()
                conn.execute('''
                    INSERT INTO citizens (fullname, id_number, dob, address, issue_date, issue_place, photo_1, photo_2)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (fullname, id_number, dob, address, issue_date, issue_place, filename1, filename2))
                conn.commit()
                conn.close()
                
                flash('Thêm mới CCCD thành công!', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('Số CCCD đã tồn tại.', 'danger')
                return redirect(request.url)
        else:
            flash('Định dạng file không hợp lệ. Chỉ chấp nhận png, jpg, jpeg.', 'danger')
            return redirect(request.url)
            
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
