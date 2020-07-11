from flask import Flask ,request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#Path where database is stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

#Database attributes with datatypes
class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(20), nullable=False, default='N/A')
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	
	def __repr__(self):
		return 'Blog post ' + str(self.id)

#Dummy data, posts to send from py file to html page
#all_posts =[
#    {
#        'title': 'Post 1',
#        'content' : ' This is the content of Post 1',
#        'author' : 'Sagar'
#    },
#    {
#        'title': 'Post 2',
#        'content' : ' This is the content of Post 2'
#    }

#]

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html',posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return "Hello, " + name + ", your id is : " + str(id)

@app.route('/onlyget', methods =['GET'])
def get_req():
    return "You can only get this webpage"

@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

if __name__ == "__main__":
    app.run(debug=True) 