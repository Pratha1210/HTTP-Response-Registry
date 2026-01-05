from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, APIResponse, SearchQuery
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key = 'moengage_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already exists', 'warning')
            return redirect(url_for('signup'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/add_api_response', methods=['GET', 'POST'])
def add_api_response():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        code = request.form['code']
        message = request.form['message']
        image_url = request.form['image_url']

        # Check if code already exists
        existing = APIResponse.query.filter_by(code=code).first()
        if existing:
            flash('This API code already exists.', 'warning')
            return redirect(url_for('add_api_response'))

        new_response = APIResponse(code=code, message=message, image_url=image_url)
        db.session.add(new_response)
        db.session.commit()
        flash('New API response added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_api_response.html')

@app.route('/search_api', methods=['GET', 'POST'])
def search_api():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    results = []
    search_query = ""

    if request.method == 'POST':
        search_query = request.form['search_query'].strip()

        if search_query:
            # Replace x with SQL wildcard %
            pattern = search_query.replace('x' , '%')

            results = APIResponse.query.filter(APIResponse.code.like(pattern)).all()

    return render_template('search_api.html', results=results, search_query=search_query)

@app.route('/save_api', methods=['POST'])
def save_api():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search_query_text = request.form['search_query'].strip()

    # Find if a search query already exists for user and query text
    search_query = SearchQuery.query.filter_by(user_id=session['user_id'], query_text=search_query_text).first()

    if not search_query:
        # If not exist, create one
        search_query = SearchQuery(user_id=session['user_id'], query_text=search_query_text)
        db.session.add(search_query)
        db.session.commit()

    flash('API Response saved!', 'success')
    return redirect(url_for('search_api'))

@app.route('/saved_searches')
def saved_searches():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    queries = SearchQuery.query.filter_by(user_id=session['user_id']).order_by(SearchQuery.created_at.desc()).all()
    return render_template('saved_searches.html', queries=queries)

@app.route('/run_saved_search/<int:query_id>')
def run_saved_search(query_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    saved_query = SearchQuery.query.get_or_404(query_id)

    pattern = saved_query.query_text.replace('x', '%')
    results = APIResponse.query.filter(APIResponse.code.like(pattern)).all()

    return render_template('search_results.html', results=results, search_query=saved_query.query_text)

@app.route('/delete_search_query/<int:query_id>', methods=['POST'])
def delete_search_query(query_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch the search query
    query = SearchQuery.query.filter_by(id=query_id, user_id=session['user_id']).first()

    if query:
        db.session.delete(query)
        db.session.commit()
        flash('Search query deleted successfully!', 'success')
    else:
        flash('Search query not found or unauthorized.', 'danger')

    return redirect(url_for('saved_searches'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':

    app.run(debug=True, port=5001)
