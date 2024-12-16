from flask import render_template, request, Blueprint
from flaskblog.models import Post, Category  # Assuming you have a Category model

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    categories = Category.query.all()  # I have added a new code here Query all categories
    return render_template('home.html', posts=posts, categories=categories)  # This code Pass categories to the template

@main.route("/about")
def about():
    return render_template('about.html', title='About')
