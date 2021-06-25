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


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('myPage.html')

@app.route('/match_record_form')
def match_record_form():
    teams_name = get_teams()
    return render_template('match_record_form.html', teams_name = teams_name)

@app.route('/match_record', methods = ["POST"])
def match_record():
    if request:
        df = get_match_record(request.form["team_name"])
        return render_template('match_record.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    else:
        return render_template('data_analysis.html')

@app.route('/toss_choose_form')
def toss_choose_form():
    venue_name = get_all_venues()
    return render_template('toss_choose_form.html', venue_name = venue_name)

@app.route('/toss_choose', methods = ["POST"])
def toss_choose():
    data = get_toss_data(request.form["venue_name"])
    return render_template('toss_choose.html', data = data)

@app.route('/average_scores')
def average_scores():
    df = get_average_scores()
    return render_template('average_scores.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/player_stats_form')
def player_stats_form():
    player_name = get_all_players()
    return render_template('player_stats_form.html', player_name = player_name)

@app.route('/player_stats', methods = ["POST"])
def player_stats():
    if request:
        df = get_player_stats(request.form["player_name"])
        return render_template('player_stats.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    else:
        return render_template('data_analysis.html')

if __name__ == '__main__':
	app.run(debug=True)