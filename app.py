import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# User authentication helpers
def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# Get comments for a post
def get_comments(post_id):
    conn = get_db_connection()
    comments = conn.execute('SELECT c.*, u.username FROM comments c LEFT JOIN users u ON c.user_id = u.id WHERE c.post_id = ? ORDER BY c.created ASC', (post_id,)).fetchall()
    conn.close()
    return [dict(c) for c in comments]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['password'])
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['password'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=[dict(p) for p in posts], user=current_user if current_user.is_authenticated else None)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    comments = get_comments(post_id)
    return render_template('post.html', post=post, comments=comments, user=current_user if current_user.is_authenticated else None)
@app.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form['content']
    # BUG 2: 500 error on special character in comment
    import re
    if not content:
        flash('Comment cannot be empty!')
    elif re.search(r'[^a-zA-Z0-9\s]', content):
        raise Exception('Special characters not allowed!')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)',
                     (post_id, current_user.id, content))
        conn.commit()
        conn.close()
        flash('Comment added!')
    return redirect(url_for('post', post_id=post_id))


@app.route('/create', methods=('GET', 'POST'))
def create():
    if not current_user.is_authenticated:
        flash('You must be logged in to create a post.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html', user=current_user)
@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # BUG 1: Allow empty password
        if not username:
            flash('Username is required!')
        elif User.get_by_username(username):
            # BUG 3: Change password if username exists, no error
            conn = get_db_connection()
            conn.execute('UPDATE users SET password = ? WHERE username = ?',
                         (generate_password_hash(password), username))
            conn.commit()
            conn.close()
            flash('Password updated for existing user.')
            return redirect(url_for('login'))
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, generate_password_hash(password)))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html', user=current_user if current_user.is_authenticated else None)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html', user=current_user if current_user.is_authenticated else None)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('index'))


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if not current_user.is_authenticated:
        flash('You must be logged in to edit posts.')
        return redirect(url_for('login'))
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post, user=current_user)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    if not current_user.is_authenticated:
        flash('You must be logged in to delete posts.')
        return redirect(url_for('login'))
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
