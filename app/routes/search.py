from flask import Blueprint, render_template, request
from app.models.recipe import Recipe

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_recipe():
    """
    根據關鍵字搜尋食譜
    - 讀取 GET 參數 `q`
    - 利用關鍵字對食譜 Title 進行模糊查詢
    - 渲染 templates/search/results.html 呈現搜尋結果
    """
    query = request.args.get('q', '')
    if query:
        recipes = Recipe.search(query)
    else:
        recipes = []
    return render_template('search/results.html', recipes=recipes, query=query)
