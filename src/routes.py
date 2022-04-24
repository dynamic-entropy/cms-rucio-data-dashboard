from flask import Blueprint, redirect, render_template

server_bp = Blueprint('main', __name__)

@server_bp.route('/')
def index():
    return render_template('index.html')
