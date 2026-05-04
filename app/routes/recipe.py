from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe
from app.models.category import Category

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    顯示所有食譜列表 (Homepage)
    - 取得所以食譜資料，渲染 index.html
    """
    recipes = Recipe.get_all()
    categories = Category.get_all()
    return render_template('index.html', recipes=recipes, categories=categories)

@recipe_bp.route('/recipe/new', methods=['GET'])
def create_recipe_page():
    """
    顯示新增食譜的表單
    - 渲染 templates/recipe/create.html
    """
    categories = Category.get_all()
    return render_template('recipe/create.html', categories=categories)

@recipe_bp.route('/recipe', methods=['POST'])
def create_recipe():
    """
    接收表單，新增食譜記錄
    - 讀取表單資料 (title, ingredients, steps, 等)
    - 驗證並寫入資料庫
    - 重新導向首頁或詳情頁
    """
    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    category_id = request.form.get('category_id')
    image_url = request.form.get('image_url')

    if not title or not ingredients or not steps:
        flash('請填寫所有必填欄位 (標題、食材、步驟)', 'error')
        categories = Category.get_all()
        return render_template('recipe/create.html', categories=categories)

    if category_id == '':
        category_id = None
    elif category_id:
        category_id = int(category_id)

    recipe = Recipe.create(
        title=title,
        ingredients=ingredients,
        steps=steps,
        category_id=category_id,
        image_url=image_url
    )
    flash('食譜新增成功！', 'success')
    return redirect(url_for('recipe.index'))

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    顯示單一食譜的詳細資訊
    - 利用 ID 查詢食譜 (包含所屬分類)
    - 渲染 templates/recipe/detail.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
    return render_template('recipe/detail.html', recipe=recipe)

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
def edit_recipe_page(id):
    """
    顯示編輯食譜的表單
    - 查詢現有食譜並預填表單
    - 渲染 templates/recipe/edit.html
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('recipe.index'))
    categories = Category.get_all()
    return render_template('recipe/edit.html', recipe=recipe, categories=categories)

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    接收表單，更新食譜記錄
    - 根據 ID 查詢現有食譜，並使用表單更新欄位
    - 重導向至該食譜的詳情頁
    """
    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    category_id = request.form.get('category_id')
    image_url = request.form.get('image_url')

    if not title or not ingredients or not steps:
        flash('請填寫所有必填欄位 (標題、食材、步驟)', 'error')
        return redirect(url_for('recipe.edit_recipe_page', id=id))

    if category_id == '':
        category_id = None
    elif category_id:
        category_id = int(category_id)

    updated_recipe = Recipe.update(
        recipe_id=id,
        title=title,
        ingredients=ingredients,
        steps=steps,
        category_id=category_id,
        image_url=image_url
    )
    if not updated_recipe:
        flash('更新失敗，找不到食譜', 'error')
        return redirect(url_for('recipe.index'))
        
    flash('食譜更新成功！', 'success')
    return redirect(url_for('recipe.recipe_detail', id=id))

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜
    - 根據 ID 刪除食譜紀錄
    - 重導向到首頁 (食譜列表)
    """
    success = Recipe.delete(id)
    if success:
        flash('食譜已刪除', 'success')
    else:
        flash('刪除失敗，找不到食譜', 'error')
    return redirect(url_for('recipe.index'))
