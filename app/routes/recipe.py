from flask import Blueprint, render_template, request, redirect, url_for, flash

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    顯示所有食譜列表 (Homepage)
    - 取得所以食譜資料，渲染 index.html
    """
    pass

@recipe_bp.route('/recipe/new', methods=['GET'])
def create_recipe_page():
    """
    顯示新增食譜的表單
    - 渲染 templates/recipe/create.html
    """
    pass

@recipe_bp.route('/recipe', methods=['POST'])
def create_recipe():
    """
    接收表單，新增食譜記錄
    - 讀取表單資料 (title, ingredients, steps, 等)
    - 驗證並寫入資料庫
    - 重新導向首頁或詳情頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    顯示單一食譜的詳細資訊
    - 利用 ID 查詢食譜 (包含所屬分類)
    - 渲染 templates/recipe/detail.html
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
def edit_recipe_page(id):
    """
    顯示編輯食譜的表單
    - 查詢現有食譜並預填表單
    - 渲染 templates/recipe/edit.html
    """
    pass

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    接收表單，更新食譜記錄
    - 根據 ID 查詢現有食譜，並使用表單更新欄位
    - 重導向至該食譜的詳情頁
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除指定食譜
    - 根據 ID 刪除食譜紀錄
    - 重導向到首頁 (食譜列表)
    """
    pass
