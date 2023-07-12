#Import Libraries
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
#Import the local route for this application
import os

Upload = "/Users/bhavy/Documents/imageUploader/static/temporary_file/"
#Configure App
app = Flask(__name__, template_folder="templates", static_folder='static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['Upload'] = Upload
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    path = db.Column(db.String, nullable = False)
    filename = db.Column(db.String, nullable = False)

    def __repr__(self):
        return '<Image %r>' %self.id

'''
Create Database
with app.app_context():
    db.create_all()
'''

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        file = request.files['file']

        filename = secure_filename(file.filename)
        path_name = os.path.join(app.config['Upload'], filename)
        print(path_name)
        file.save(path_name)
        print(path_name)

        new_image = Image(path = path_name, filename = filename)
        try:
            db.session.add(new_image)
            db.session.commit()
            
            return redirect("/")

        except:
            return 'There was a problem'
        
    else:
        images = Image.query.order_by(Image.id).all()
        return render_template('index.html', images = images)

@app.route('/delete/<int:id>')  
def delete(id):
    file = Image.query.get_or_404(id)
    try:
        os.remove(file.path)
        db.session.delete(file)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting your file'
    
if __name__ == "__main__":
    app.run(debug=True)
