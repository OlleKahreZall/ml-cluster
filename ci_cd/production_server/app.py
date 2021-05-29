import numpy as np
from flask import Flask, render_template
import pickle
from workerA import get_accuracy_logreg, get_predictions_logreg

app = Flask(__name__)
model = pickle.load(open('model-logreg.sav', 'rb'))

@app.route('/')
def home():
    predictions = get_predictions_logreg()
    return render_template('front-page.html')

#To use the predict button in our web-app
@app.route("/predictions", methods=['POST'])
def predictions():
    predictions = get_predictions_logreg()
    accuracy = get_accuracy_logreg()
    return render_template('predictions-page.html', accuracy=accuracy, final_results = predictions)  

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port=5100,debug=True)