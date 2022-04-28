from flask import Flask, render_template, request, Response, send_file, after_this_request, flash
import pandas as pd
import requests
import os
from matplotlib.image import imread
import random
from shutil import copyfile
from keras.preprocessing.image import ImageDataGenerator as datagen
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model

application = app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file')
            return render_template(
                'home.html'
            )
        request.files['file'].save(os.path.join('photo/', request.files['file'].filename))
        path = 'photo/' + str(request.files['file'].filename)

        img = load_img(path, target_size=(224, 224))
        img = img_to_array(img)
        img = img.reshape(1, 224, 224, 3)
        img = img.astype('float32')
        img = img - [123.68, 116.779, 103.939]

        #model = pickle.load(open('model/demo_model.pkl', 'rb'))
        model = load_model('model/demo_model.h5')
        result_raw = model.predict(img)
        if result_raw[0][0] == 1.0:
            result = 'DOG'
        else:
            result = 'CAT'
        print(result_raw)
        return render_template(
            'results.html',
            result=result
        )
    return render_template(
        'home.html'
    )

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 80, debug = True)
