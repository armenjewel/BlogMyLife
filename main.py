from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret" 
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:justblogit@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'as9d8F7d98C3f7a'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    submitted = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, unique=True)

    def __init__(self, title, body, submitted=True):
        self.title = title
        self.body = body
        self.submitted = submitted
        self.owner = owner_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.Column(db.String(2000))

    def __init__(self, username, password, blogs):
        self.username = username
        self.password = password
        self.blogs = blogs

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
def home():
    blog_id = request.args.get('id')
    submitted_blogs = Blog.query.all()
    return render_template('login.html', submitted_blogs=submitted_blogs)

@app.route('/index', methods=['POST', 'GET'])
def index():
    #blog_id = request.args.get('id')
    all_users = User.query.all()
    return render_template('index.html', all_users=all_users)


    """blog_id = request.args.get('id')
    submitted_blogs = Blog.query.all()
    return render_template('index.html', submitted_blogs=submitted_blogs)"""

@app.route('/blog', methods=['POST', 'GET'])
def show_posts(): 
    title = ''
    body = ''
    if request.method == 'GET':
   
        submitted_blogs = Blog.query.all()
        return render_template('blog.html', submitted_blogs=submitted_blogs, title=title, body=body)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title = ''
    body = ''
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        submitted = True
        owner_id = user.id
        newpost = Blog(title=title, body=body, submitted=True, owner_id=owner_id)
        db.session.add(newpost)
        db.session.commit()
        blog=newpost.id
        blogs=Blogs(title=title, body=body)
        return redirect('/blog?id={0}'.format(blog))
    else:
        return render_template('newpost.html', title='title', body='body')

"""
New Routes Below
"""

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('Error: User password incorrect, or user does not exist')
            return redirect('/login')    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        blogs = ['']
        # TODO - validate user's data
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password, blogs)
            db.session.add(new_user)
            db.session.commit()
            user=new_user.id
            session['username'] = username
            return redirect('/user?id={0}'.format(user))
            return redirect('/newpost')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"
        error = []
        if len(username) < 3:
            flash('Username must be between 3 and 30 characters')
            return redirect('/')
        if password != verify_password:
            flash('Passwords must match')
            return redirect('/signup')
        if len(username) < 1 or len(password) < 1 or len(verify_password) < 1 or len(email) < 1:
            flash('You must complete the information from all fields')
            return redirect('/')
        for char in username or char in email or char in password:
            if char == " ":
                flash('Invalid character: Your password may not contain a space')
                return redirect('/')                
        if len(username) <3 or len(password) < 3 or len(username) > 20 or len(password) > 20:
            flash('Username and Password must be between 3-20 characters')
            return redirect('/signup')            
        else:
            session['username'] = username 
            flash("Welcome", + username)
            return redirect('/blog')
    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')
# @app.route('/delete-entry', methods=['POST'])
# def delete_entry():

#     blog_id = int(request.form['entry-id'])
#     entry = Blog.query.filter_by(title)
#     Blog.completed = False
#     db.session.delete(entry)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    app.run()
