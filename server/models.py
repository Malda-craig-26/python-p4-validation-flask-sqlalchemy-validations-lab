from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, _, name):
        if not name:
            raise ValueError("Author name must be provided")
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("No two authors should have the same name")
        return name

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates('phone_number')
    def validate_phone_number(self, _, phone_number):
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(phone_number) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self,_ , title):
        if not title:
            raise ValueError("Title must be provided")
        existing_post = Post.query.filter_by(title=title).first()
        if existing_post and existing_post.id != self.id:
            raise ValueError("No two posts should have the same title")
        return title
    
    @validates('content')
    def validate_content(self, _, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return content
    
    @validates('summary')
    def validate_summary(self,_ , summary):
        if len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters long")
        return summary
    
    @validates('category')
    def validate_category(self, _, category):
        valid_categories = ['Fiction', 'Non-Fiction']
        if category not in valid_categories:
            raise ValueError(f"Category must be either Fiction or non-Fiction")
        return category
    
    @validates('title')
    def validate_title(self, _, title):
        clickbait_phrases = [
            "Won't Believe", "Secret", "Top", "Guess"
        ]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait")
        return title
    
    

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
