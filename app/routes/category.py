from flask import Blueprint, render_template, request, redirect, url_for, flash

category_bp = Blueprint('category', __name__)

@category_bp.route('/category', methods=['GET'])
def list_categories():
    """
    顯示所有分類列表
    - 取得分類列表並渲染 templates/category/list.html
    """
    pass

@category_bp.route('/category', methods=['POST'])
def create_category():
    """
    接收表單，新增分類記錄
    - 驗證分類名稱是否重複
    - 新增分類，重新導向該列表頁
    """
    pass

@category_bp.route('/category/<int:id>', methods=['GET'])
def category_detail(id):
    """
    顯示特定分類下的食譜清單
    - 查詢有此分類 ID 的食譜，渲染類似 index 的表單
    """
    pass
