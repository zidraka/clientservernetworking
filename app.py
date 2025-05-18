from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
import os
import psutil

app = Flask(__name__)
Bootstrap(app)

# Folder video dalam folder static/video
VIDEO_FOLDER = os.path.join(app.static_folder, 'video')

# Fungsi untuk mendapatkan semua file video
def get_video_files():
    files = []
    for filename in os.listdir(VIDEO_FOLDER):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            filepath = os.path.join(VIDEO_FOLDER, filename)
            size_bytes = os.path.getsize(filepath)
            files.append({
                'name': filename,
                'size': size_bytes,  # ukuran dalam byte
                'type': os.path.splitext(filename)[1][1:].upper()
            })
    return files

@app.route('/')
def index():
    files = get_video_files()  # Ambil video untuk index juga jika ingin ditampilkan
    return render_template('index.html', files=files)

@app.route('/dashboard')
def dashboard():
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    files = get_video_files()  # daftar video untuk dashboard
    return render_template('dashboard.html', cpu=cpu_usage, memory=mem_usage, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(VIDEO_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
