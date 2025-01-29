from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
import os, json



@post_bp.route('/')
def get_posts():
    posts = read_posts()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    posts = read_posts()
    post = next((post for post in posts if post["id"] == id), None)

    if post is None:
        abort(404)

    return render_template("detail_post.html", post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = {
            "id": get_new_id(),
            "title": form.title.data,
            "content": form.content.data,
            "category": form.category.data,
            "is_active": form.is_active.data,
            "publication_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "author": session.get('username', 'Unknown')
        }

        posts = read_posts()
        posts.append(new_post)
        write_posts(posts)

        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template('add_post.html', form=form)





def get_posts_file_path():
    """Повертає шлях до файлу posts.json відносно кореня блюпринта."""
    return os.path.join(post_bp.root_path, 'posts.json')

def read_posts():
    """Зчитує всі пости з JSON-файлу."""
    posts_file = get_posts_file_path()
    if os.path.exists(posts_file):
        with open(posts_file, 'r') as file:
            return json.load(file)
    return []

def write_posts(posts):
    """Записує список постів у JSON-файл."""
    posts_file = get_posts_file_path()
    with open(posts_file, 'w') as file:
        json.dump(posts, file, indent=4)


def get_new_id():
    """Генерує новий унікальний ID для поста"""
    posts = read_posts()
    if posts:
        return max(post['id'] for post in posts) + 1
    return 1