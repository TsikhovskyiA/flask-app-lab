from app import db
from datetime import datetime as dt

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=dt.now)  # Передаємо функцію без виклику
    is_active = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(100), nullable=False, default='None')
    author = db.Column(db.String(100), nullable=False, default='Unknown')

    def __repr__(self):
        # Форматування часу до секунд
        posted_str = self.posted.strftime('%Y-%m-%d %H:%M:%S') if self.posted else 'N/A'
        return f"<Post(title={self.title}, posted={posted_str})>"
