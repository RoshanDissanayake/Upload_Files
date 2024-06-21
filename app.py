from flask import Flask, request, render_template_string, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Upload Files</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
      body {
        background-color: #f8f9fa;
      }
      .container {
        margin-top: 50px;
      }
      h1, h2 {
        margin-bottom: 30px;
      }
      ul {
        list-style-type: none;
        padding: 0;
      }
      ul li {
        margin-bottom: 10px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Upload Files</h1>
      <form method="post" action="/upload" enctype="multipart/form-data">
        <div class="form-group">
          <input type="file" name="files" class="form-control-file" multiple>
        </div>
        <button type="submit" class="btn btn-primary">Upload</button>
      </form>
      <h2>Uploaded Files</h2>
      <ul>
        {% for file in files %}
          <li><a href="{{ url_for('uploaded_file', filename=file) }}">{{ file }}</a></li>
        {% endfor %}
      </ul>
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
    if 'files' not in request.files:
        return 'No file part'
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            return 'No selected file'
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
