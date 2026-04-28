from app import db


class Category(db.Model):
    """食譜分類 Model"""
    __tablename__ = 'categories'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, nullable=False,
                            server_default=db.func.now())

    # 關聯：一個分類有多個食譜
    recipes = db.relationship('Recipe', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

    # ── CRUD 方法 ─────────────────────────────────────────────

    @classmethod
    def create(cls, name: str, description: str = None) -> 'Category':
        """新增一個分類"""
        category = cls(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_all(cls) -> list['Category']:
        """取得所有分類（依名稱排序）"""
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, category_id: int) -> 'Category | None':
        """依 ID 取得分類"""
        return cls.query.get(category_id)

    @classmethod
    def update(cls, category_id: int, name: str,
               description: str = None) -> 'Category | None':
        """更新分類資訊"""
        category = cls.get_by_id(category_id)
        if category is None:
            return None
        category.name = name
        category.description = description
        db.session.commit()
        return category

    @classmethod
    def delete(cls, category_id: int) -> bool:
        """刪除指定分類，食譜的 category_id 將自動設為 NULL"""
        category = cls.get_by_id(category_id)
        if category is None:
            return False
        db.session.delete(category)
        db.session.commit()
        return True
