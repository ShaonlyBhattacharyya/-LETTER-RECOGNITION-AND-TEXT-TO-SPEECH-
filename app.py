from flask import Flask, flash, request, redirect, url_for, render_template 
import urllib.request 
import os 
import secrets 
from gtts import gTTS 
from werkzeug.utils import secure_filename 
from WordsToText import img2text as i2t 
 
app = Flask(__name__) 
 
UPLOAD_FOLDER = 'D:/Project/Minor/Minor_Proj/' 
AUDIO_FOLDER = 'D:/Project/Minor/Minor_Proj/static/audios/' 
 
app.secret_key = "secret key" 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER 
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) 
 
 
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
 
 
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
        text = i2t(filename) 
        tts = gTTS(text) 
        gen_aud_fname = secrets.token_hex(10) + ".mp3" 
        file_loc = (os.path.join(app.config['AUDIO_FOLDER'], gen_aud_fname)) 
        tts.save(file_loc) 
        return render_template('index.html', filename = filename, audio = True, file = 
gen_aud_fname) 
    else: 
        flash('Allowed image types are - png, jpg, jpeg') 
        return redirect(request.url) 
 
@app.route('/display/<filename>') 
def display_image(filename): 
    return redirect(url_for('Minor', filename='Minor_Proj/' + filename), code=301) 
if __name__ == "__main__": 
    app.run() 