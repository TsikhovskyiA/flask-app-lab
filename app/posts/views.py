from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
from .model import Post, Tag
from app.users.models import User
from app import db
from flask import request
from datetime import datetime, timezone




@post_bp.route('/')
def get_posts():
    stmt= db.select(Post).order_by(Post.posted)
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    stmt = db.select(Post).where(Post.id == id)
    post = db.session.scalar(stmt)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    # Отримати всіх користувачів із бази даних
    form.author.choices = [(user.id, user.username) for user in User.query.all()]
    
    # Заповнення списку тегів
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    
    if form.validate_on_submit():
        # Створення нового поста
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data or datetime.utcnow(timezone.utc),  # Значення за замовчуванням
            user_id=form.author.data  # ID автора, вибраного з форми
        )
        
        # Додавання вибраних тегів
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags.extend(selected_tags)
        
        # Збереження змін у базі даних
        db.session.add(new_post)
        db.session.commit()

        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))  # Перенаправлення на список постів

    return render_template('add_post.html', form=form)




@post_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    # Отримуємо пост з бази даних або повертаємо 404
    post = db.session.get(Post, id)
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('.get_posts'))

    # Ініціалізація форми з даними поста
    form = PostForm(obj=post)

    # Попереднє встановлення дати для `publish_date`
    if request.method == 'GET':  # Тільки при першому завантаженні форми
        form.publish_date.data = post.posted

    # Обробка відправленої форми
    if form.validate_on_submit():
        # Оновлення полів поста
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.posted = form.publish_date.data

        # Збереження змін у базі даних
        db.session.commit()

        # Повідомлення про успішне оновлення
        flash('Post updated successfully', 'success')
        return redirect(url_for('.get_posts'))

    # Рендеринг шаблону з формою
    return render_template("add_post.html", form=form, post=post)

@post_bp.route('/<int:id>/delete', methods=['POST'])
def delete_post(id):
    # Отримуємо пост з бази даних або повертаємо 404
    post = db.session.get(Post, id)
    if not post:
        flash('Post not found', 'danger')
        return redirect(url_for('.get_posts'))

    # Видаляємо пост із бази даних
    db.session.delete(post)
    db.session.commit()

    # Повідомлення про успішне видалення
    flash('Post deleted successfully', 'success')
    return redirect(url_for('.get_posts'))
