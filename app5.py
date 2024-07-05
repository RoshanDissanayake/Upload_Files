from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = 'images'  # Specify the folder for static files

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Expense Bills</title>
    <style>
        body {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin-top: 10px;
            color: #333;
        }
        input[type="text"], input[type="date"], input[type="file"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4caf50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
        }
        button:hover {
            background-color: #45a049;
        }
        img.logo {
            display: block;
            margin: 0 auto;
            max-width: 100px;
            height: auto;
        }
        .file-list {
            margin-top: 20px;
        }
        .file-item {
            margin-bottom: 5px;
        }
        @media (max-width: 600px) {
            .container {
                padding: 10px;
                max-width: 90%;
            }
            input[type="text"], input[type="date"], input[type="file"] {
                width: calc(100% - 12px);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="/static/images/logo.png" alt="Logo" class="logo">
        <h1>Upload Expense Bills</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="uploader_name">Uploader Name:</label>
            <input type="text" id="uploader_name" name="uploader_name" required>
            <br>
            <label for="upload_date">Upload Date:</label>
            <input type="date" id="upload_date" name="upload_date" required>
            <br>
            <label for="files">Select files:</label>
            <input type="file" id="files" name="files" multiple required>
            <br>
            <button type="submit">Upload</button>
        </form>
        
        <div class="file-list">
            {% if files %}
                <h2>Uploaded Files:</h2>
                <ul>
                {% for file in files %}
                    <li class="file-item">{{ file }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No files uploaded yet.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploader_name = request.form['uploader_name']
    upload_date = request.form['upload_date']
    if 'files' not in request.files:
        return 'No file part'
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            continue
        if file:
            _, file_extension = os.path.splitext(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{uploader_name}_{timestamp}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=7777)
