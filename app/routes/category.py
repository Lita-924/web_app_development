from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.category import Category
from app.models.recipe import Recipe

category_bp = Blueprint('category', __name__)

@category_bp.route('/category', methods=['GET'])
def list_categories():
    """
    顯示所有分類列表
    - 取得分類列表並渲染 templates/category/list.html
    """
    categories = Category.get_all()
    return render_template('category/list.html', categories=categories)

@category_bp.route('/category', methods=['POST'])
def create_category():
    """
    接收表單，新增分類記錄
    - 驗證分類名稱是否重複
    - 新增分類，重新導向該列表頁
    """
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('分類名稱不能為空', 'error')
        return redirect(url_for('category.list_categories'))
        
    existing = Category.query.filter_by(name=name).first()
    if existing:
        flash('該分類名稱已存在', 'error')
        return redirect(url_for('category.list_categories'))
        
    Category.create(name=name, description=description)
    flash('分類新增成功！', 'success')
    return redirect(url_for('category.list_categories'))

@category_bp.route('/category/<int:id>', methods=['GET'])
def category_detail(id):
    """
    顯示特定分類下的食譜清單
    - 查詢有此分類 ID 的食譜，渲染類似 index 的表單
    """
    category = Category.get_by_id(id)
    if not category:
        flash('找不到該分類', 'error')
        return redirect(url_for('recipe.index'))
    return redirect(url_for('recipe.index', category_id=id))
