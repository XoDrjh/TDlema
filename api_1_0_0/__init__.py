from . import database
db = database.DataBase('nuaadiandao')

from flask import Blueprint
api = Blueprint('api_1_0_0', __name__)

from .route import *

