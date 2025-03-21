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
                image_paths[f'image{i}'] = os.path.join('uploads', filename) 

        yearly = request.form.get('yearly')
        volume = request.form.get('volume')
        issue = request.form.get('issue')
        month = request.form.get('month')
        issue_text = request.form.get('issue_text')
        first_para = request.form.get('first_para')
        second_para = request.form.get('second_para')
        
        topics = {}
        descriptions = {}
        main_headings = {}
        training_images = {}
        for i in range(1, 73):
            file = request.files.get(f'training_img{i}')
            top = request.form.get(f'topic{i}')
            main_head =  request.form.get(f'trp{i}')
            main_headings[f'main_head{i}'] = main_head

            # print(top)
            topics[f'topic{i}'] = top
            description = request.form.get(f'description{i}')
            descriptions[f'description{i}'] = description
            if file and allowed_file(file.filename):
                filename = f'training_img{i}.{file.filename.rsplit(".", 1)[1].lower()}'
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                training_images[f'training_img{i}'] = os.path.join('uploads', filename)
        

        
            
        print('last pic',descriptions['description5'])
        

        return render_template('mag.html',fp = first_para,
                               sp = second_para, image_paths=image_paths,
                                 yearly=yearly, volume=volume, issue=issue,
                                   month=month, issue_text=issue_text,
                                training_images=training_images,
                                topics = topics,descriptions = descriptions,
                                main_headings = main_headings)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
