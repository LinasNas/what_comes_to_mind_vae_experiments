from flask import session, make_response #stores user

import numpy as np
import random
from .models import Player, Board

#gets current user from data
def current_user():
    return session.get("user")

#gets player.id object for current user, if none return none.
def current():
    return Player.get_or_none(Player.id == current_user())

#gets board associated with player, if none return none.
def current_board():
    return Board.get_or_none(Board.player == current_user())

#setting up api_errors.
def api_error(message, status=404, **kwargs):
    response = {"message": message, **kwargs}
    return make_response(response, status)


def softmax(x, temperature=0.1):
    e_x = np.exp(np.array(x) / temperature)
    return e_x / e_x.sum(axis=0)