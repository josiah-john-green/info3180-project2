from app import app, db, login_manager
from flask import Flask, request, jsonify, session, redirect, url_for, flash, send_from_directory, render_template, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app.models import User
from app.forms import RegistrationForm
from datetime import datetime, timezone


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# API route for user registration
@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegistrationForm()
    
    if form.validate():
        profile_photo = form.profile_photo.data
        filename = secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User(
            username=form.username.data, 
            password=form.password.data, 
            firstname=form.firstname.data, 
            lastname=form.lastname.data, 
            email=form.email.data, 
            location=form.location.data, 
            biography=form.biography.data, 
            profile_photo=filename, 
            joined_on=datetime.now()
        )
        
        db.session.add(user)
        db.session.commit()

        response_data = {
            "message": "User successfully registered",
            "username": form.username.data, 
            "firstname": form.firstname.data, 
            "lastname": form.lastname.data, 
            "email": form.email.data, 
            "location": form.location.data, 
            "biography": form.biography.data, 
            "profile_photo": filename, 
            "joined_on": user.joined_on
        }
        return jsonify(response_data), 201
        
    else:
        errors = form_errors(form)
        return jsonify({'errors': errors}), 400


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
