from flask import Blueprint

bp = Blueprint('memories', __name__)

from diary.memories import routes