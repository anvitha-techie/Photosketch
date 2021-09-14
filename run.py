import cv2
from flask import Flask, flash, request, redirect, url_for, render_template,app
import urllib.request
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__,static_url_path="/static")
#run_with_ngrok(app)
 
UPLOAD_FOLDER = 'static/uploads/'
DOWNLOAD_FOLDER = 'static/downloads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(path, filename):
  photosktch(path, filename)

def photosktch(path, filename):
  img = cv2.imread(path, 1)
  img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  img2=cv2.bitwise_not(img_gray)
  img_smooth=cv2.GaussianBlur(img2,(21,21),sigmaX=25,sigmaY=25)
  final_img=cv2.divide(img_gray, 255 - img_smooth, scale=256)
  cv2.imwrite(f"{DOWNLOAD_FOLDER}{filename}",final_img)

     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        process_file(os.path.join(UPLOAD_FOLDER,filename),filename)
        #data={
          #"processed_img":'static/downloads/'+filename,
          #"uploaded_img":'static/uploads/'+filename
         #}
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='downloads/' + filename), code=301)
if __name__ == '__main__':
    app.run()
