import os
import time
import random
import numpy as np
import torch
import datetime
# from eval import *
from eval import generate, models, word_index
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, session

# https://j2logo.com/tutorial-flask-leccion-17-desplegar-flask-produccion-nginx-gunicorn/

# from applicationinsights import TelemetryClient
# from applicationinsights.requests import WSGIApplication
# from applicationinsights.exceptions import enable

from miscc.config import cfg
#from werkzeug.contrib.profiler import ProfilerMiddleware
from botocore.client import Config
import boto3
from dotenv import dotenv_values



# enable(os.environ["TELEMETRY"])
app = Flask(__name__)
app.secret_key = 'mermelada'
# app.wsgi_app = WSGIApplication(os.environ["TELEMETRY"], app.wsgi_app)

config = dotenv_values(".env") 
ACCESS_KEY_ID = config["ACCESS_KEY_ID"]
ACCESS_SECRET_KEY = config["ACCESS_SECRET_KEY"]
BUCKET_NAME = "scopicbucket"

# @app.route('/api/v1.0/bird', methods=['POST'])
# def create_bird():
#     if not request.json or not 'caption' in request.json:
#         abort(400)

#     caption = request.json['caption']

#     t0 = time.time()
#     urls = generate(caption, wordtoix, ixtoword, text_encoder, netG, s3)
#     t1 = time.time()

#     response = {
#         'small': urls[0],
#         'medium': urls[1],
#         'large': urls[2],
#         'map1': urls[3],
#         'map2': urls[4],
#         'caption': caption,
#         'elapsed': t1 - t0
#     }
#     return jsonify({'bird': response}), 201

# @app.route('/api/v1.0/birds', methods=['POST'])
# def create_birds():
#     if not request.json or not 'caption' in request.json:
#         abort(400)

#     caption = request.json['caption']

#     t0 = time.time()
#     urls = generate(caption, wordtoix, ixtoword, text_encoder, netG, s3, copies=6)
#     t1 = time.time()

#     response = {
#         'bird1' : { 'small': urls[0], 'medium': urls[1], 'large': urls[2] },
#         'bird2' : { 'small': urls[3], 'medium': urls[4], 'large': urls[5] },
#         'bird3' : { 'small': urls[6], 'medium': urls[7], 'large': urls[8] },
#         'bird4' : { 'small': urls[9], 'medium': urls[10], 'large': urls[11] },
#         'bird5' : { 'small': urls[12], 'medium': urls[13], 'large': urls[14] },
#         'bird6' : { 'small': urls[15], 'medium': urls[16], 'large': urls[17] },
#         'caption': caption,
#         'elapsed': t1 - t0
#     }
#     return jsonify({'bird': response}), 201


@app.route('/', methods=['GET', 'POST'])
def get_bird():    
    if request.method == 'POST':        
        caption = request.form['caption'] 
        t0 = time.time()
        urls = generate(caption, wordtoix, ixtoword, text_encoder, netG, s3)
        t1 = time.time()       
        # url ="https://scopicbucket.s3.sa-east-1.amazonaws.com/output/2023/June/07/23_31_17_586757/bird_g2.png"
        # url = f"https://scopicbucket.s3.sa-east-1.amazonaws.com/{urls[0]}"
        print("url: ", urls[0])
        session['caption'] = caption
        session['url'] = urls[2]
        print("caption: ", caption)        
        return redirect('/generated')
    return render_template('index.html')

@app.route('/generated', methods=['GET', 'POST'])
def get_generated():
    caption = session.get('caption')
    url = session.get('url')
    if request.method == 'POST':
        print(caption)
        return redirect('/')
    return render_template('image.html', caption=caption, url=url)

if __name__ == '__main__':
    caption = "*"
    t0 = time.time()
    # tc = TelemetryClient(os.environ["TELEMETRY"])
    
    # gpu based
    # cfg.CUDA = os.environ["GPU"].lower() == 'true'
    # tc.track_event('container initializing', {"CUDA": str(cfg.CUDA)})

    # load word dictionaries
    wordtoix, ixtoword = word_index()
    # lead models
    text_encoder, netG = models(len(wordtoix))
    # load blob service
    
    # blob_service = BlockBlobService(account_name='attgan', account_key=os.environ["BLOB_KEY"])
    
    s3 = boto3.resource('s3', aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY, config=Config(signature_version='s3v4'))

    seed = 100
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if cfg.CUDA:
        torch.cuda.manual_seed_all(seed)

    #app.config['PROFILE'] = True
    #app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    #app.run(host='0.0.0.0', port=8080, debug = True)

    t1 = time.time()
    # tc.track_event('container start', {"starttime": str(t1-t0)})
    app.run(host='0.0.0.0', port=5000)
