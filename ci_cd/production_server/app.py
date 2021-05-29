from flask import Flask, render_template
import os
from workerA import get_metrics
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('front-page.html')

#To use the predict button in our web-app
@app.route("/predictions", methods=['POST'])
def predictions():
    r2,top_repos,time_elapsed = get_metrics()
    #print("HELLO EVERYONE",time_elapsed)
    return render_template('predictions-page.html',
                            r2_bagging = r2[0],
                            r2_gradboost = r2[1],
                            r2_neural_network = r2[2],
                            r2_voting = r2[3],
                            r2_tree = r2[4],
                            r2_random_forest = r2[5],
                            rep1_name = top_repos[0][0],
                            rep1_pred_stars = top_repos[1][0],
                            rep1_real_stars = top_repos[2][0],
                            rep1_forks = top_repos[3][0],
                            rep1_subscribers = top_repos[4][0],
                            rep2_name =  top_repos[0][1],
                            rep2_pred_stars = top_repos[1][1],
                            rep2_real_stars = top_repos[2][1],
                            rep2_forks = top_repos[3][1],
                            rep2_subscribers = top_repos[4][1],
                            rep3_name =  top_repos[0][2],
                            rep3_pred_stars = top_repos[1][2],
                            rep3_real_stars = top_repos[2][2],
                            rep3_forks = top_repos[3][2],
                            rep3_subscribers = top_repos[4][2],
                            rep4_name =  top_repos[0][3],
                            rep4_pred_stars = top_repos[1][3],
                            rep4_real_stars = top_repos[2][3],
                            rep4_forks = top_repos[3][3],
                            rep4_subscribers = top_repos[4][3],
                            rep5_name =  top_repos[0][4],
                            rep5_pred_stars = top_repos[1][4],
                            rep5_real_stars = top_repos[2][4],
                            rep5_forks = top_repos[3][4],
                            rep5_subscribers = top_repos[4][4],
                            time_elapsed = np.round(time_elapsed,3))

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5100))
    app.run(host='0.0.0.0', port=5100, debug=True)

