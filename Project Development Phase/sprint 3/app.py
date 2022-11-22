# import numpy as np
# import pandas as pd
# import pickle
from flask import Flask,request,render_template,jsonify
import requests
from math import ceil
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)
# model = pickle.load(open('CKD_NLP.pkl','rb'))
# with gzip.open("CKD_NLP.pkl", 'rb') as f:
#     model = pickle.load(f, fix_imports=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=["POST"])
def prediction():
    red_blood_cells = int(request.form['red_blood_cells'])
    pus_cell = int(request.form['pus_cell'])
    blood_glucose_random = int(request.form['blood_glucose_random'])
    blood_urea = int(request.form['blood_urea'])
    pedal_edema = int(request.form['pedal_edema'])
    anemia = int(request.form['anemia'])
    diabetesmellitus = int(request.form['diabetesmellitus'])
    coronary_artery_disease = int(request.form['coronary_artery_disease'])
    input_features = list()
    input_features.append(red_blood_cells)
    input_features.append(pus_cell)
    input_features.append(blood_glucose_random)
    input_features.append(blood_urea)
    input_features.append(pedal_edema)
    input_features.append(anemia)
    input_features.append(diabetesmellitus)
    input_features.append(coronary_artery_disease)
    features_value = list()
    features_name = ["red_blood_cells","pus_cell","blood_glucose_random","blood_urea","pedal_edema","anemia","diabetesmellitus","coronary_artery_disease"]
    features_value.append(input_features)
    API_KEY = "vYu2qAz8-CQNDi6aDjPyXrJ_jDe5eYcMSXRD7Af7QW0Y"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    payload_scoring = {"input_data": [{"fields": features_name, "values": features_value}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/250bd1eb-6f57-4ab3-9233-a0bb8ba16299/predictions?version=2022-11-22', json=payload_scoring,headers=header)
    prediction = response_scoring.json()['predictions'][0]['values'][0][0]
    if prediction == 1:
        prob = response_scoring.json()['predictions'][0]['values'][0][1][1]
    else:
        prob = response_scoring.json()['predictions'][0]['values'][0][1][0]
    arg_red_blood_cells = "Normal" if int(request.form['red_blood_cells']) == 1 else "Abnormal"
    arg_pus_cell = "Normal" if int(request.form['pus_cell']) == 1 else "Abnormal"
    arg_blood_glucose_random = int(request.form['blood_glucose_random'])
    arg_blood_urea = int(request.form['blood_urea'])
    arg_pedal_edema = "Yes" if int(request.form['pedal_edema']) == 1 else "No"
    arg_anemia = "Yes" if int(request.form['anemia']) == 1 else "No"
    arg_diabetesmellitus = "Yes" if int(request.form['diabetesmellitus']) == 1 else "No"
    arg_coronary_artery_disease = "Yes" if int(request.form['coronary_artery_disease']) == 1 else "No"
    if prediction == 0:
        return render_template('predictionckd.html',prob=ceil(prob*100),arg_red_blood_cells=arg_red_blood_cells,arg_pus_cell=arg_pus_cell,arg_blood_glucose_random=arg_blood_glucose_random,arg_blood_urea=arg_blood_urea,arg_pedal_edema=arg_pedal_edema,arg_anemia=arg_anemia,arg_diabetesmellitus=arg_diabetesmellitus,arg_coronary_artery_disease=arg_coronary_artery_disease)
    else:
        return render_template('predictionnockd.html',prob=ceil(prob*100),arg_red_blood_cells=arg_red_blood_cells,arg_pus_cell=arg_pus_cell,arg_blood_glucose_random=arg_blood_glucose_random,arg_blood_urea=arg_blood_urea,arg_pedal_edema=arg_pedal_edema,arg_anemia=arg_anemia,arg_diabetesmellitus=arg_diabetesmellitus,arg_coronary_artery_disease=arg_coronary_artery_disease)

@app.route('/send_mail', methods=["GET"])
def send_mail():
    arg_red_blood_cells = request.args.get('arg_red_blood_cells')
    arg_pus_cell = request.args.get('arg_pus_cell')
    arg_blood_glucose_random = request.args.get('arg_blood_glucose_random')
    arg_blood_urea = request.args.get('arg_blood_urea')
    arg_pedal_edema = request.args.get('arg_pedal_edema')
    arg_anemia = request.args.get('arg_anemia')
    arg_diabetesmellitus = request.args.get('arg_diabetesmellitus')
    arg_coronary_artery_disease = request.args.get('arg_coronary_artery_disease')
    prediction = int(request.args.get('prediction'))
    if prediction == 1:
        res = "You're chances of having Chronic Kidney Disease is less"
    else:
        res = "You may have Chronic Kidney Disease"
    email_sender = 'voidmain0101@gmail.com'
    email_password = 'jmstflysyvizxubl'
    email_receiver = request.args.get('email')
    subject = 'Kidney Disease Prediction Report'
    body = "Red Blood Cells : " + arg_red_blood_cells + "\nPus Cells : " + arg_pus_cell + "\nBlood Glucose : " + arg_blood_glucose_random + "\nBlood Urea : " + arg_blood_urea + "\nPedal Edema : " + arg_pedal_edema + "\nAnemia : " + arg_anemia + "\nDiabetes : " + arg_diabetesmellitus + "\nCoronary Artery Disease : " + arg_coronary_artery_disease + "\nPrediction : " + res
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    return jsonify({'mail':'sent'})

if __name__ == '__main__':
    app.run(debug=True)