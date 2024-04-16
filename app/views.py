from flask import Flask, request, jsonify, session, redirect, url_for, flash, render_template
from .models import User, Post, Like, Follow
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt

from app import app, db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# API Routes

@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    location = data.get('location')
    biography = data.get('biography')
    profile_photo = data.get('profile_photo')
    joined_on = datetime.utcnow()

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409

    new_user = User(username=username, password=generate_password_hash(password), firstname=firstname, lastname=lastname, email=email, location=location, biography=biography, profile_photo=profile_photo, joined_on=joined_on)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    # Implement logout functionality, e.g., clearing the session or token
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
def create_post(user_id):
    data = request.get_json()
    caption = data.get('caption')
    photo = data.get('photo')

    post = Post(caption=caption, photo=photo, user_id=user_id, created_on=datetime.utcnow())
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    posts = Post.query.filter_by(user_id=user_id).all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    user_id = session['user_id']
    like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    if not like:
        like = Like(post_id=post_id, user_id=user_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'message': 'Post liked successfully'})
    else:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message': 'Post unlike successfully'})

@app.route('/api/v1/users/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    follower_id = session['user_id']
    follow = Follow.query.filter_by(follower_id=follower_id, user_id=user_id).first()
    if not follow:
        follow = Follow(follower_id=follower_id, user_id=user_id)
        db.session.add(follow)
        db.session.commit()
        return jsonify({'message': 'User followed successfully'})
    else:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'message': 'User unfollowed successfully'})

# Frontend Routes

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        # Handle user registration
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # Handle user login
        token = login_user(request.form['username'], request.form['password'])
        if token:
            session['token'] = token
            return redirect(url_for('explore_page'))
        else:
            # Display error message
            flash('Invalid Login credentials')
            pass
    return render_template('login.html')

@app.route('/logout')
def logout_page():
    # Handle user logout
    session.pop('token', None)
    return redirect(url_for('index'))

@app.route('/explore')
def explore_page():
    # Display all posts
    posts = get_all_posts()
    return render_template('explore.html', posts=posts)

@app.route('/users/<int:user_id>')
def user_profile_page(user_id):
    # Display user profile and posts
    user = User.query.get(user_id)
    posts = get_user_posts(user_id)
    return render_template('user_profile.html', user=user, posts=posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post_page():
    if request.method == 'POST':
        # Handle new post creation
        create_post(session['user_id'], request.form['caption'], request.form['photo'])
        return redirect(url_for('explore_page'))
    return render_template('new_post.html')