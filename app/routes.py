# app/routes.py

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file
from .utils import process_video, add_user, check_user_credentials, update_user_password, find_user_by_email, save_feedback, get_all_feedback, save_detected_filter, get_happy_clients_count, get_videos_analyzed_count, increment_videos_analyzed_count
import os
import threading
from datetime import datetime

bp = Blueprint('main', __name__)

# Routes for Signup, Login, Logout
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if add_user(email, password):
            flash('Account created successfully!', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('User already exists.', 'danger')
    return render_template('signup.html')

# Other routes (login, home, etc.) can be added in a similar way

# Don't forget to add the route for `apply_filter`, `get_filters`, etc., here.
