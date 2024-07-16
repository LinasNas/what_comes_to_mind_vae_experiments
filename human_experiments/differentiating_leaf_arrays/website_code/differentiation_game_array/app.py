from flask import Flask, redirect, render_template, request, session, jsonify
from models import db, Player, GameReward
from api import api
import datetime
import json 
import os 

app = Flask(__name__)
app.secret_key = 'example_secret_key'
app.register_blueprint(api, url_prefix='/api')

env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if request.method == 'POST':
        new_player = Player.create(consent=datetime.datetime.now())
        session['player_id'] = new_player.id
        print(f'New player ID: {new_player.id}')
        return redirect('/introduction_1')
    return render_template('consent.html')

@app.route('/introduction_1')
def introduction_1(): 
    return render_template('introduction_1.html')

@app.route('/game_1_introduction_1')
def game_1_introduction_1(): 
    return render_template('game_1_introduction_1.html')

@app.route('/game_1', methods=['GET', 'POST'])
def game_1():
    player_id = session.get('player_id')

    if request.method == 'POST':
        data = request.get_json()
        print("Received data:", data)

        player = Player.get_or_none(Player.id == player_id)
        if player and 'rewards' in data and isinstance(data['rewards'], dict):
            for image_name, reward in data['rewards'].items():
                GameReward.get_or_create(player=player, image_name=image_name, defaults={'reward': reward})
            
            high_reward = data.get('high_reward')
            low_reward = data.get('low_reward')

            if high_reward is not None:
                player.high_reward = high_reward
                player.low_reward = low_reward
                player.save()

            return jsonify({"status": "success"})
        else:
            return jsonify({"error": "Invalid data or player not found"}), 404

    return render_template('game_1.html', player_id=player_id)

@app.route('/game_2')
def game_2():
    player_id = session.get('player_id')
    player = Player.get_or_none(Player.id == player_id)
    if player:
        rewards_query = GameReward.select().where(GameReward.player == player)
        rewards = {reward.image_name: reward.reward for reward in rewards_query}
        print("Rewards for game_2:", rewards)
        return render_template('game_2.html', player_id=player_id, rewards=rewards)
    else:
        return "Player not found", 404

@app.route('/task_intro')
def task_intro():
    return render_template('task_intro.html')

@app.route('/task_main')
def task_main():
    player_id = session.get('player_id')
    player = Player.get_or_none(Player.id == player_id)
    if player:
        rewards_query = GameReward.select().where(GameReward.player == player)
        rewards = {reward.image_name: reward.reward for reward in rewards_query}
        return render_template('task_main.html', rewards=rewards)
    else:
        return "Player not found", 404
    
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    player_id = session.get('player_id')
    if not player_id:
        return jsonify({"error": "Player session not found"}), 404
    
    data = request.get_json()
    answer = data.get('answer')
    if not answer:
        return jsonify({"error": "No answer provided"}), 400

    try:
        player = Player.get_by_id(player_id)
        more_different = answer
        less_different = "peach" if answer == "grape" else "grape"
        player.more_different = more_different
        player.less_different = less_different
        player.save()
        return jsonify({"status": "success"})
    except Player.DoesNotExist:
        return jsonify({"error": "Player not found"}), 404

@app.route('/save_total_reward', methods=['POST'])
def save_total_reward():
    data = request.get_json()
    player_id = data.get('player_id')
    total_payoff = data.get('total_payoff')

    player = Player.get_or_none(Player.id == player_id)
    if player:
        player.total_payoff = total_payoff
        player.save()
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "Player not found"}), 404


@app.route('/submit_mturk_id', methods=['POST'])
def submit_mturk_id():
    data = request.get_json()
    player_id = session.get('player_id')
    mturk_id = data.get('mturk_id')

    player = Player.get_or_none(Player.id == player_id)
    if player:
        player.mturk_id = mturk_id
        player.save()
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "Player not found"}), 404

@app.route('/bonus')
def bonus():
    return render_template('bonus.html')

@app.route('/terminate')
def terminate():
    player_id = session.get('player_id')
    if not player_id:
        return "Player session not found", 404
    try:
        player = Player.get_by_id(player_id)
        print(f'Terminating session for player ID: {player_id}')

        return render_template('terminate.html')
    except Player.DoesNotExist:
        return "Player not found", 404

if __name__ == '__main__':
    app.run(debug=True)
