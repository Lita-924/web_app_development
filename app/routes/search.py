from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_recipe():
    """
    根據關鍵字搜尋食譜
    - 讀取 GET 參數 `q`
    - 利用關鍵字對食譜 Title 進行模糊查詢
    - 渲染 templates/search/results.html 呈現搜尋結果
    """
    pass
