from flask import Flask, render_template
import os
from workerA import get_metrics

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('front-page.html')

#To use the predict button in our web-app
@app.route("/predictions", methods=['POST'])
def predictions():
    r2, mse = get_metrics()

    return render_template('predictions-page.html',
                            r2_bagging = r2[0],
                            mse_bagging = mse[0],
                            r2_gradboost = r2[1],
                            mse_gradboost = mse[1],
                            r2_neural_network = r2[2],
                            mse_neural_network = mse[2],
                            # r2_svm = r2[3],
                            # mse_svm = mse[3],
                            r2_voting = r2[3],
                            mse_voting = mse[3])

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5100))
    app.run(host='0.0.0.0', port=5100, debug=True)