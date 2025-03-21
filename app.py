from flask import Flask, request, render_template, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_paths = {}
        for i in range(1, 8):
            file = request.files.get(f'event_img{i}')
            if file and allowed_file(file.filename):
                filename = f'event_img{i}.{file.filename.rsplit(".", 1)[1].lower()}'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_paths[f'image{i}'] = os.path.join('uploads', filename)  # Save path relative to static

        yearly = request.form.get('yearly')
        volume = request.form.get('volume')
        issue = request.form.get('issue')
        month = request.form.get('month')
        issue_text = request.form.get('issue_text')
        
        return render_template('mag.html', image_paths=image_paths, yearly=yearly, volume=volume, issue=issue, month=month, issue_text=issue_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
