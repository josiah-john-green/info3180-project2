from app import app, db, login_manager
from flask import Flask, request, jsonify, session, redirect, url_for, flash, send_from_directory, render_template, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm, PostForm
from datetime import datetime, timezone


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# API route for user registration
@app.route('/api/v1/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    location = request.form.get('location')
    biography = request.form.get('biography')
    profile_photo = request.files.get('profile_photo')

    # Save the uploaded profile photo to a directory
    if profile_photo:
        filename = secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = ''  # Set a default value if no profile photo is uploaded

    user = User(
        username=username,
        password=password,
        firstname=firstname,
        lastname=lastname,
        email=email,
        location=location,
        biography=biography,
        profile_photo=filename
    )

    db.session.add(user)
    db.session.commit()

    response_data = {
        "message": "User successfully registered",
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "location": location,
        "biography": biography,
        "profile_photo": filename,
        "joined_on": user.joined_on
    }
    return jsonify(response_data), 201


# API route for user login
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        errors = form_errors(form)
        return jsonify({'errors': errors}), 400


# API route to check if user exists
@app.route('/api/v1/user/<username>', methods=['GET'])
def check_user_exists(username):
    # Query the database to check if the user exists
    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'exists': True}), 200
    else:
        return jsonify({'exists': False}), 404


# API route to load user
@login_manager.user_loader
@login_required
def load_user(username):
    return User.query.filter_by(username=username).first()


# API route for user logout
@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Assuming you're using Flask-Login for session management
    return jsonify({'message': 'Logged out successfully'}), 200


##
# Functions for posts creation and retrival.
##

# API route to fetch user_id by username
@app.route('/api/v1/users/<string:username>/id')
def get_user_id(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'user_id': user.id})
    else:
        return jsonify({'error': 'User not found'}), 404


# API route for post creation
@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@login_required
def post(user_id):
    caption = request.form.get('caption')
    photo = request.files.get('photo')

    # Save the uploaded profile photo to a directory
    if photo:
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = ''  # Set a default value if no profile photo is uploaded

    # Create a new Post object and associate it with the user
    post = Post(
        caption=caption,
        photo=filename,
        user_id=user_id
    )

    db.session.add(post)  # Add the post to the database
    db.session.commit()    # Commit the transaction

    response_data = {
        "message": "Post submitted successfully",
        "caption": caption,
        "photo": filename,
        "post_id": post.id  # Optionally return the ID of the newly created post
    }
    return jsonify(response_data), 201


##
# Functions for token creation in API's and Web Forms.
##


# API route for retrieving CSRF token
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


##
# Functions for file handling.
##


# API route for serving uploaded poster images
@app.route('/api/v1/photos/<filename>')
def get_photo(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


##
# Functions for error, and request handling.
##


# Error function for form.
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages


# Handle 404 Not Found errors
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Not found'}), 404


# Handle 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500
