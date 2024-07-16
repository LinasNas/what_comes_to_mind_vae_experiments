from flask import Blueprint, request, jsonify
from models import Player, GameReward

api = Blueprint('api', __name__)

@api.route('/save_rewards', methods=['POST'])
def save_rewards():
    data = request.json
    player_id = data.get('player_id')
    rewards_data = data.get('rewards')
    print("Saving rewards for player_id:", player_id, "Rewards:", rewards_data)

    try:
        player = Player.get(Player.id == player_id)
        for image_name, reward in rewards_data.items():
            GameReward.get_or_create(player=player, image_name=image_name, defaults={'reward': reward})
        return jsonify({"message": "Rewards saved successfully"}), 200
    except Player.DoesNotExist:
        return jsonify({"error": "Player not found"}), 404

@api.route('/get_rewards', methods=['GET'])
def get_rewards():
    player_id = request.args.get('player_id')
    print("Retrieving rewards for player_id:", player_id)
    try:
        player = Player.get(Player.id == player_id)
        rewards = GameReward.select().where(GameReward.player == player)
        rewards_dict = {reward.image_name: reward.reward for reward in rewards}
        return jsonify(rewards_dict), 200
    except Player.DoesNotExist:
        return jsonify({"error": "Player not found"}), 404