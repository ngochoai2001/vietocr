import os

from flask import Flask, request, abort, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from predict_processor import vietocr_text_recognition, loadPredictor
from model.auth import UserLoginRequest, UserRegistrationRequest
from schema import user_serializer, users_serializer
from core.config import user_db, image_db
from craft_text_detector import load_refinenet_model,load_craftnet_model
from transformers import pipeline
 
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
CURRENT_DICECTORY = os.getcwd()
UPLOAD_FOLDER =os.path.join(CURRENT_DICECTORY, 'static/user_img')
CRAFT_REFINE_NET = load_refinenet_model(cuda=False)
CRAFT_NET = load_craftnet_model(cuda=False, weight_path='./craft_mlt_25k.pth')
PREDICTOR = loadPredictor
CORRECTOR = pipeline("text2text-generation", model="bmd1905/vietnamese-correction")

def is_extensions_allowed(filename):
    return '.' in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route("/media/upload/", methods = ["POST"])
def upload_img():
    

    if 'file' not in request.files:
        return jsonify({"error_message": "media not provided"}), 400
    file = request.files['file']
    if file.filename =='':
        return jsonify({"error_message": "media not provided"}), 400
    filename = secure_filename(file.filename)
    print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    result = vietocr_text_recognition(os.path.join(app.config['UPLOAD_FOLDER'], filename), CRAFT_REFINE_NET, CRAFT_NET, PREDICTOR, CORRECTOR)
    return jsonify({"result":result}), 200


@app.route("/login/", methods = "GET")
def login(user: UserLoginRequest):
    user = user_db.find_one({
        "user_name": user.user_name,
        "pass_word": user.pass_word
    })
    if(user):
        return {
            "status": "Login successfully",
            "data": user_serializer(user)
        }
    # else:
        # raise HTTPException(
        #     status_code=404, detail="Login failed, pls check you username and password"
        # )

if __name__ == "__main__":
    app.run(debug=True, port=8000)

