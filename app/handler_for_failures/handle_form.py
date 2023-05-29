from flask import (
    Blueprint, flash, g, redirect, render_template, url_for, request, session
)

from app import logger

bp = Blueprint('formhandler', __name__, url_prefix='/')

@bp.get('')
def index():
    return "Hello, I'm handler"

