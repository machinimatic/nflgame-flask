import json
import nflgame
import nfldb
import requests
import sys
from flask import Flask, request, jsonify
from flask import render_template
app = Flask(__name__)

db = nfldb.connect()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/_search_by_year/<season_year>/<season_type>/<season_week>")
def search_year(season_year, season_type, season_week):
    q = nfldb.Query(db)

    name = request.args.get('name')
    year = int(season_year)
    week = int(season_week)

    q.game(season_year=year, season_type=season_type, week=week)
    games = q.as_players()
    player_list = []
    for player in games:
        if player.full_name.lower().startswith(name) or player.last_name.lower().startswith(name):
            data = {'label': player.full_name, 'value': player.full_name, 'id': player.player_id}
            player_list.append(data)
    return jsonify(matching_results=player_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
