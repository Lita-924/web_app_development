from flask import Blueprint, render_template, abort
from app.models.recipe import Recipe

share_bp = Blueprint('share', __name__)

@share_bp.route('/share/<share_token>', methods=['GET'])
def share_recipe(share_token):
    """
    顯示利用 UUID 產生的唯讀食譜分享頁面
    - 根據 share_token 查出食譜，找不到回傳 404
    - 渲染 templates/recipe/share.html
    - 頁面內不包含修改和刪除功能
    """
    recipe = Recipe.get_by_token(share_token)
    if not recipe:
        abort(404)
    return render_template('recipe/share.html', recipe=recipe)
