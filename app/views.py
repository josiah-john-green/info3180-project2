"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/

This file creates your application.
"""


import os
import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from datetime import datetime
from app import app, db, login_manager
from flask import render_template, request, jsonify, send_file, session, send_from_directory, url_for, redirect, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.forms import LoginForm, RegistrationForm, NewPostForm
from app.models import User, Post, Follow, Like
from flask_wtf.csrf import generate_csrf


##
# Functions for authorisation.
##

# 
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


# 
@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


#
@app.route('/api/v1/register', methods=['POST'])
def register():
    
    """Accepts user information and saves it to the database"""
    registrationForm = RegistrationForm()

    if registrationForm.validate_on_submit():
        # Extract form data
        username = registrationForm.username.data
        password = registrationForm.password.data
        firstname = registrationForm.firstname.data
        lastname = registrationForm.lastname.data
        email = registrationForm.email.data
        location = registrationForm.location.data
        biography = registrationForm.biography.data
        photo = registrationForm.profile_photo.data
        
        if photo:
            # Save the profile photo to the uploads folder
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ''  # Set a default value if no photo is uploaded
        
        joined_on = datetime.utcnow()
        
        # Create a new User object with the profile photo path
        user = User(username, password, firstname, lastname, email, location, biography, filename, joined_on)

        # Add the user to the session and commit
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User successfully registered.",
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "location": location,
            "biography": biography,
            "profile_photo": filename,  # Send the path instead of the FileStorage object
            "joined_on": joined_on
        }), 201

    errors = form_errors(registrationForm)
    return jsonify(errors=errors), 400


# 
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    
    """Accepts login credentials as username and password"""
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
        
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            jwt_token = generate_token(user.id)
        
            return jsonify({
                "message": "User successfully logged in.",
                "token": jwt_token
            }), 200
        
        return jsonify(errors=["Invalid username or password"])
    
    errors = form_errors(loginForm)
    return jsonify(errors=errors), 400


# Define the logout route
@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required  # Ensure the user is logged in to log out
def logout():
    try:
        # Perform logout operations
        logout_user()  # Log out the user
        
        # Return a success message
        return jsonify({"message": "User successfully logged out."}), 200

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "Logout failed", "details": str(e)}), 500


##
# Functions for post creation and retrieval.
##

# 
@login_manager.user_loader
def load_user(user_id):
    # Query the database for the user by user ID
    return User.query.get(int(user_id))


# API route for creating a new post
@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@login_required
@requires_auth
def add_post(user_id):
    postForm = NewPostForm()

    if postForm.validate_on_submit():
        photo = postForm.photo.data
        caption = postForm.caption.data

        # Save the uploaded photo to a directory
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ''  # Set a default value if no photo is uploaded

        created_on = datetime.now()

        # Create a new post object with explicit column names
        post = Post(user_id=user_id, 
                    caption=caption, 
                    photo=filename, 
                    created_on=created_on)

        # Add the post to the session and commit
        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "Successfully created a new post"}), 201

    errors = form_errors(postForm)
    return jsonify(errors=errors), 400

# Route to get a specific post by its ID
@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
@login_required
@requires_auth
def get_post_with_user(post_id):
    try:
        # Fetch the post and user details
        post = db.session.execute(
            db.select(Post).filter_by(id=post_id)
        ).scalar()

        if not post:
            return jsonify({"error": "Post not found"}), 404

        user = db.session.execute(
            db.select(User).filter_by(id=post.user_id)
        ).scalar()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if the current user has liked the post
        user_has_liked = (
            db.session.execute(
                db.select(Like).filter_by(post_id=post_id, user_id=current_user.id)
            ).scalar() is not None
        )

        # Prepare the post data with user information
        post_data = {
            "id": post.id,
            "photo": url_for("get_photo", filename=post.photo),
            "caption": post.caption,
            "created_on": post.created_on.strftime("%d %B %Y"),
            "user": {
                "id": user.id,
                "username": user.username,
                "profile_photo": url_for("get_photo", filename=user.profile_photo),
            },
        }

        return jsonify(post_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route for a specific person's posts
@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
@login_required
@requires_auth
def get_posts(user_id):
    
    # Query posts for the specified user
    posts = Post.query.filter_by(user_id=user_id).all()

    post_list = []
    
    for post in posts:
        post_data = {
            'id': post.id,
            'user_id': post.user_id,
            'photo': post.photo,
            'caption': post.caption,
            'created_on': post.created_on.strftime('%d %B, %Y')
        }
        post_list.append(post_data)
        
    return jsonify(post_list), 200


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@login_required
@requires_auth
def get_user_details(user_id):

    # Ensure user_id is a valid integer
    user_details = db.session.execute(db.select(User).filter_by(id=int(user_id))).scalar()

    if not user_details:
        return jsonify({"error": "User not found"}), 404

    # Return user details and other information
    return jsonify({
        "id": user_details.id,
        "username": user_details.username,
        "firstname": user_details.firstname,
        "lastname": user_details.lastname,
        "email": user_details.email,
        "location": user_details.location,
        "biography": user_details.biography,
        "profile_photo": url_for('get_photo', filename=user_details.profile_photo),
        "joined_on": user_details.joined_on.strftime('%B %Y'),
        "posts": [
            {
                "id": post.id,
                "photo": url_for('get_photo', filename=post.photo),
                "user_id": post.user_id,
                "caption": post.caption,
                "created_on": post.created_on
            }
            for post in db.session.execute(db.select(Post).filter_by(user_id=user_details.id)).scalars()
        ],
    }), 200
    

# API route for viewing all posts
@app.route('/api/v1/posts', methods=['GET'])
@login_required
@requires_auth
def get_all_posts():
    """Return all posts for all users"""

    posts = db.session.execute(db.select(Post)).scalars()

    all_posts = []
    
    for post in posts:
        likes = db.session.execute(db.select(Like).filter_by(id=post.id)).scalars()

        user = db.session.execute(db.select(User).filter_by(id=post.user_id)).scalar()

        all_posts.append({
            "id": post.id,
            "user_id": post.user_id,
            "profile_photo": url_for("get_photo", filename=user.profile_photo),
            "username": user.username,
            "photo": url_for("get_photo", filename=post.photo),
            "caption": post.caption,
            "created_on": post.created_on.strftime('%d %B %Y'),  # Format datetime directly here
            "likes": len([like for like in likes])
        })

    return jsonify(all_posts), 200


##
# Functions for likes.
##


# API route for likes
@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@login_required
@requires_auth
def like(post_id):
    user_id = int(current_user.get_id())

    # Check if the user has already liked the post
    like = db.session.execute(
        db.select(Like).filter_by(post_id=post_id, user_id=user_id)
    ).scalar()

    if like:
        # If already liked, remove the like
        db.session.delete(like)
        db.session.commit()
        message = "Post unliked!"
    else:
        # If not liked yet, add a like
        new_like = Like(post_id=post_id, user_id=user_id)
        db.session.add(new_like)
        db.session.commit()
        message = "Post liked!"

    return jsonify({"message": message}), 200


# API route for counting likes 
@app.route('/api/v1/posts/<int:post_id>/like', methods=['GET'])
@login_required
def get_like_count(post_id):
    # Count the number of followers for the target user
    like_count = db.session.query(Like).filter_by(post_id=post_id).count()

    return jsonify({
        "likes": like_count,
    }), 200

# API route for checking if a user has liked a post
@app.route('/api/v1/posts/<int:post_id>/like_status', methods=['GET'])
@login_required
def get_like_status(post_id):
    try:
        # Check if the current user has liked the specified post
        has_liked = Like.query.filter_by(
            user_id=current_user.id,
            post_id=post_id
        ).first() is not None  # Determine if there's a like record for the user and post
        
        # Return the like status
        return jsonify({"has_liked": has_liked}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors and return a 500 status code


##
# Functions for follow.
##


# API route for following a user
@app.route('/api/v1/users/<user_id>/follow', methods=['POST'])
@login_required
def follow(user_id):
    current_user_id = int(current_user.get_id())

    if current_user_id == int(user_id):
        return jsonify({"error": "You can't follow yourself."}), 400

    # Check if the follow relationship already exists
    existing_follow = db.session.query(Follow).filter_by(follower_id=current_user_id, user_id=user_id).first()

    if existing_follow:
        db.session.delete(existing_follow)  # Unfollow if already following
        db.session.commit()
        return jsonify({"message": "Unfollowed successfully."})

    # Create a new follow relationship if not following
    new_follow = Follow(follower_id=current_user_id, user_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({"message": "You are now following that user."})


# API route for counting followers 
@app.route('/api/v1/users/<int:user_id>/follow', methods=['GET'])
@login_required
def get_follower_count(user_id):
    # Count the number of followers for the target user
    follower_count = db.session.query(Follow).filter_by(user_id=user_id).count()

    return jsonify({
        "followers": follower_count,
    }), 200


# API route for checking the following status
@app.route('/api/v1/users/<int:user_id>/follow_status', methods=['GET'])
@login_required
def follow_status(user_id):
    try:
        user_to_check = User.query.get_or_404(user_id)  # Fetch the user
        
        is_following = Follow.query.filter_by(
            follower_id=current_user.id,
            user_id=user_to_check.id
        ).first() is not None  # Check if the current user follows the target user
        return jsonify({"is_following": is_following}), 200  # Return the follow status
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors

##
# Functions for token creation in API's and Web Forms.
##


# API route for retrieving CSRF token
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    try:
        csrf_token = generate_csrf()  # Ensure this function call works correctly
        return jsonify({'csrf_token': csrf_token})  # Return valid JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Catch any errors and return 500


# API route for generatiing JWT token
def generate_token(uid):
    timestamp = datetime.utcnow()
    payload = {
        "subject": uid,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=60)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


##
# Functions for file handling.
##


# API route for serving uploaded photos
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
