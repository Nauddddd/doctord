import email
from venv import create
from warnings import catch_warnings
from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from building_pro2.models.diagnostic import Diagnosis
from flask_login import login_required, current_user
from .predict import predict_image
import os, cv2 as cv
from . import db
from uuid import uuid4
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import base64

from PIL import Image



main = Blueprint('main', __name__)


UPLOAD_FOLDER = 'CLOUD/uploads'
PREDICTION_FOLDER = 'CLOUD/predictions'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    date = current_user._created
    created = date.strftime("%d %B %Y")
    return render_template('profile.html', name = current_user.username, email = current_user.email, created = created)

@main.route('/guide')
def guide():
    return render_template('guide.html')

@main.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    # history = Diagnosis.query.filter_by(_creator=current_user._id).all()
    history = Diagnosis.query.filter_by(_creator=current_user._id).order_by(Diagnosis._created.desc()).paginate(page=page, per_page=5)
    # history.reverse()
    histories = []
    for i in history.items:
        id = i._id
        tm = i._created
        time = datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second, 0)
        time = time + timedelta(seconds=0)
        histories += [{'id':id, 'time':time}]
    print(histories)
    return render_template('history.html', histories = histories, posts = history)

@main.route("/upload-image", methods=["GET"])
@login_required
def upload_image():
    return render_template("upload.html")

@main.route("/upload-image", methods=["POST"])
@login_required
def upload_image_post():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        img = cv.imread(os.path.join(UPLOAD_FOLDER, filename))
        prediction = predict_image(img)
        prediction = prediction[:,:,::-1]
        prediction = Image.fromarray(prediction)
        prediction.save(os.path.join(PREDICTION_FOLDER, filename))
        # ============================================================
        _id = uuid4()
        _created = datetime.now()
        _deleted = None
        _creator = current_user.get_id()
        path = os.path.join(PREDICTION_FOLDER, filename)

        new_diagnosis = Diagnosis(_id =_id, _created = _created, _deleted = _deleted, _creator = _creator, path = path)

        db.session.add(new_diagnosis)
        db.session.commit()

        # ============================================================
        with open(os.path.join(PREDICTION_FOLDER, filename), 'rb') as f:
            data = f.read()

        content = base64.b64encode(data).decode('utf-8')
        image = {
                "content": content,
                "file_name":filename
            }
        return render_template('detail.html', image=image)

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@main.route("/detail-{id}", methods=["GET"])
@login_required
def detail():
    id = request.args.get('id')
    try:
        record = Diagnosis.query.filter_by(_id=id).first()
    except:
        record = None    
    if record:
        with open(record.path, 'rb') as f:
            data = f.read()

        content = base64.b64encode(data).decode('utf-8')
        image = {
                "content": content,
                "file_name":record.path.split('/')[-1]
            }
        return render_template('detail.html', image=image)
    else:
        return redirect(url_for('main.history'))