import requests

API_KEY = "vYu2qAz8-CQNDi6aDjPyXrJ_jDe5eYcMSXRD7Af7QW0Y"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

payload_scoring = {"input_data": [{"fields": ["red_blood_cells","pus_cell","blood_glucose_random","blood_urea","pedal_edema","anemia","diabetesmellitus","coronary_artery_disease"], "values": [[1,1,93,66,0,0,1,0]]}]}

#payload_scoring = {"input_data": [{"fields": 
# ["red_blood_cells","pus_cell","blood_glucose_random","blood_urea","pedal_edema","anemia","diabetesmellitus","coronary_artery_disease"], 
# "values": [[1,1,87,38,0,0,0,0]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/250bd1eb-6f57-4ab3-9233-a0bb8ba16299/predictions?version=2022-11-22', json=payload_scoring,headers=header)

print("Scoring response")
prediction = response_scoring.json()['predictions'][0]['values'][0][0]
if prediction == 1:
    prob = response_scoring.json()['predictions'][0]['values'][0][1][1]
else:
    prob = response_scoring.json()['predictions'][0]['values'][0][1][0]
print(prediction)
print(prob)