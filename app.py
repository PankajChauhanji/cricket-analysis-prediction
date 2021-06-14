# Importing essential libraries
from flask import Flask, send_file, make_response, render_template, request
import os
from src.util import *
from src.plot import *

env = os.getenv("run_env", "dev")

if env == "dev":
    BASE_URL = "http://localhost:5000/"
elif env == "prod":
    BASE_URL = "google.com"

app = Flask(__name__)

# To handle home page.
@app.route('/')
def home():
	return render_template('index.html')

#To handle prediction page.
@app.route('/prediction')
def prediction():
    venues = get_venues()
    teams = get_teams()
    return render_template('prediction.html', venues = venues, teams = teams)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        final_score = predict_final_score(request)
        return render_template('result.html', lower_limit = final_score-5, upper_limit = final_score+5)

# TO handle data analysis Page.
# get data to keep it in memory, usually you will serve this from a database or bucket, or whereever your db is sitting
breast_cancer_df, features_names = get_breast_cancer_df()

@app.route('/data_analysis')
def data_analysis():
    return render_template('data_analysis.html', base_url = BASE_URL)

@app.route('/plots/breast_cancer_data/pairplot/features/<features>', methods=['GET'])
def pairplot(features):
    try:
        # parse columns
        parsed_features = [feature.strip() for feature in features.split(',')]
        bytes_obj = get_pair_plot_as_bytes(breast_cancer_df, parsed_features)

        return send_file(bytes_obj,
                         attachment_filename='plot.png',
                         mimetype='image/png')
    except ValueError:
        # something went wrong to return bad request
        return make_response('Unsupported request, probably feature names are wrong', 400)

if __name__ == '__main__':
	app.run(debug=True)