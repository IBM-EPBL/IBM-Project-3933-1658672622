import numpy as np
import pandas as pd
from flask import Flask,request,render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('CKD_NLP.pkl','rb'))
# with gzip.open("CKD_NLP.pkl", 'rb') as f:
#     model = pickle.load(f, fix_imports=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=["POST"])
def prediction():
    blood_urea = float(request.form['blood_urea'])
    blood_glucose_random = float(request.form['blood_glucose_random'])
    coronary_artery_disease = int(request.form['coronary_artery_disease'])
    anemia = int(request.form['anemia'])
    pus_cell = int(request.form['pus_cell'])
    red_blood_cells = int(request.form['red_blood_cells'])
    diabetesmellitus = int(request.form['diabetesmellitus'])
    pedal_edema = int(request.form['pedal_edema'])
    input_features = list()
    input_features.append(red_blood_cells)
    input_features.append(pus_cell)
    input_features.append(blood_glucose_random)
    input_features.append(blood_urea)
    input_features.append(pedal_edema)
    input_features.append(anemia)
    input_features.append(diabetesmellitus)
    input_features.append(coronary_artery_disease)
    features_value = [np.array(input_features)]
    
    features_name = ["red_blood_cells","pus_cell","blood_glucose_random","blood_urea","pedal_edema","anemia","diabetesmellitus","coronary_artery_disease"]
    df = pd.DataFrame(features_value,columns=features_name)
    output = model.predict(df)
    if output[0] == 0:
        return render_template('predictionckd.html')
    else:
        return render_template('predictionnockd.html')

if __name__ == '__main__':
    app.run(debug=True)