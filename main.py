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

@app.route("/_render_player_info")
def render_player_info():
    name = request.args.get('name')
    birthdate = request.args.get('birthdate')
    college = request.args.get('college')
    profile_url = request.args.get('profile_url')
    team = request.args.get('team')
    uniform_number = request.args.get('uniform_number')
    weight = request.args.get('weight')
    years_pro = request.args.get('years_pro')
    return render_template('player_info.html',
            name=name,
            birthdate=birthdate,
            college=college,
            profile_url=profile_url,
            team=team,
            uniform_number=uniform_number,
            weight=weight,
            years_pro=years_pro)

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
        print dir(player)
        if player.first_name.lower().startswith(name) or player.last_name.lower().startswith(name):
            data = {
                    'label': player.full_name,
                    'value': player.full_name,
                    'id': player.player_id,
                    'first_name': player.first_name,
                    'last_name': player.last_name,
                    'birthdate': player.birthdate,
                    'college': player.college,
                    'profile_url': player.profile_url,
                    'team': player.team,
                    'uniform_number': player.uniform_number,
                    'weight': player.weight,
                    'years_pro': player.years_pro
                    }
            player_list.append(data)
    return jsonify(matching_results=player_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
