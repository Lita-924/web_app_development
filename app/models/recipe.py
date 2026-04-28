import uuid
from datetime import datetime

from app import db


class Recipe(db.Model):
    """食譜 Model"""
    __tablename__ = 'recipes'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title       = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps       = db.Column(db.Text, nullable=False)
    image_url   = db.Column(db.Text, nullable=True)
    share_token = db.Column(db.Text, nullable=False, unique=True,
                            default=lambda: str(uuid.uuid4()))
    category_id = db.Column(db.Integer,
                             db.ForeignKey('categories.id', ondelete='SET NULL'),
                             nullable=True)
    created_at  = db.Column(db.DateTime, nullable=False,
                             default=datetime.now)
    updated_at  = db.Column(db.DateTime, nullable=False,
                             default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Recipe {self.title}>'

    # ── CRUD 方法 ─────────────────────────────────────────────

    @classmethod
    def create(cls, title: str, ingredients: str, steps: str,
               category_id: int = None, image_url: str = None) -> 'Recipe':
        """新增一筆食譜（自動產生 share_token）"""
        recipe = cls(
            title=title,
            ingredients=ingredients,
            steps=steps,
            category_id=category_id,
            image_url=image_url,
            share_token=str(uuid.uuid4()),
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_all(cls, category_id: int = None) -> list['Recipe']:
        """取得所有食譜，可依分類篩選"""
        query = cls.query.order_by(cls.created_at.desc())
        if category_id is not None:
            query = query.filter_by(category_id=category_id)
        return query.all()

    @classmethod
    def get_by_id(cls, recipe_id: int) -> 'Recipe | None':
        """依 ID 取得食譜"""
        return cls.query.get(recipe_id)

    @classmethod
    def get_by_token(cls, share_token: str) -> 'Recipe | None':
        """依 share_token 取得食譜（分享頁面用）"""
        return cls.query.filter_by(share_token=share_token).first()

    @classmethod
    def search(cls, keyword: str) -> list['Recipe']:
        """依關鍵字搜尋食譜標題"""
        pattern = f'%{keyword}%'
        return (cls.query
                .filter(cls.title.like(pattern))
                .order_by(cls.created_at.desc())
                .all())

    @classmethod
    def update(cls, recipe_id: int, title: str, ingredients: str,
               steps: str, category_id: int = None,
               image_url: str = None) -> 'Recipe | None':
        """更新食譜內容"""
        recipe = cls.get_by_id(recipe_id)
        if recipe is None:
            return None
        recipe.title       = title
        recipe.ingredients = ingredients
        recipe.steps       = steps
        recipe.category_id = category_id
        recipe.image_url   = image_url
        recipe.updated_at  = datetime.now()
        db.session.commit()
        return recipe

    @classmethod
    def delete(cls, recipe_id: int) -> bool:
        """刪除指定食譜"""
        recipe = cls.get_by_id(recipe_id)
        if recipe is None:
            return False
        db.session.delete(recipe)
        db.session.commit()
        return True
