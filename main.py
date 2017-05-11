import json
import nflgame
import nfldb
import requests
from stat_names import stat_names
import sys
from flask import Flask, request, jsonify, session
from flask import render_template
app = Flask(__name__)
app.config.from_envvar('NFLGAME_APP_SETTINGS')

db = nfldb.connect()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/player/<player_id>")
@app.route("/player/<player_id>/<int:year>")
@app.route("/player/<player_id>/<int:year>/<phase>")
@app.route("/player/<player_id>/<int:year>/<phase>/<int:week>")
def render_player_info(player_id, year="All", phase="All", week="All"):
    player = nfldb.Player.from_id(db, player_id)
    q = nfldb.Query(db).game()

    if (phase == "Preseason") or (phase == "Regular") or (phase == "Postseason"):
        q.game(season_type=phase)
    if 2009 <= int(year) <= 2016:
        q.game(season_year=year)
    if 1 <= int(week) <= 17:
        q.game(week=week)

    q.player(gsis_name=player.gsis_name, team=player.team)
    stats = q.as_aggregate()

    stat_list = {}
    for stat in stats:
        for field in stat.fields:
            # Reverse this so it joins properly with category list
            stat_list[field] = int(getattr(stat, field))

    session['prev_year'] = year
    session['prev_phase'] = phase
    session['prev_week'] = week
    session['prev_player_id'] = str(player.player_id)
    session['prev_player_name'] = str(player.full_name)

    return render_template('player.html', player=player, stats=stat_list, stat_names=stat_names, session=session)

@app.route("/_render_player_stats/<player_id>")
def render_player_stats(player_id):
    pass

@app.route("/_search_player")
def search_player():
    name = request.args.get('name')

    player_list = []

    player, dist = nfldb.player_search(db, name)
    data = {
            'label': player.full_name + " (" + player.team + ", " + str(player.position) + ")",
            'value': player.full_name,
            'id': player.player_id,
            }
    player_list.append(data)

    return jsonify(matching_results=player_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
