# 路由設計文件：食譜收藏夾 (Recipe Collection System)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 / 食譜列表 | GET | / | templates/index.html | 顯示所有食譜列表 |
| 新增食譜頁面 | GET | /recipe/new | templates/recipe/create.html | 顯示新增食譜的表單 |
| 建立食譜 | POST | /recipe | — | 接收表單並存入資料庫，建立後重導向至食譜列表或詳情頁 |
| 食譜詳情 | GET | /recipe/<int:id> | templates/recipe/detail.html | 顯示單一食譜的詳細資訊 |
| 編輯食譜頁面 | GET | /recipe/<int:id>/edit | templates/recipe/edit.html | 顯示編輯食譜的表單 |
| 更新食譜 | POST | /recipe/<int:id>/update | — | 接收表單並更新資料庫，更新後重導向至食譜詳情頁 |
| 刪除食譜 | POST | /recipe/<int:id>/delete | — | 刪除食譜，完成後重導向至食譜列表 |
| 搜尋食譜 | GET | /search | templates/search/results.html | 根據關鍵字搜尋食譜並顯示結果 |
| 分類列表 | GET | /category | templates/category/list.html | 顯示所有分類 |
| 新增分類 | POST | /category | — | 接收表單，新增分類，完成後重導向回分類列表 |
| 分類詳情 | GET | /category/<int:id> | templates/index.html | 顯示特定分類下的食譜列表 |
| 唯讀分享頁 | GET | /share/<share_token> | templates/recipe/share.html | 顯示利用 UUID 產生的唯讀分享食譜頁面 |

## 2. 每個路由的詳細說明

### Recipe 模組 (`/recipe`)
- **新增食譜 (POST /recipe)**: 
  - 輸入：表單欄位 (`title`, `ingredients`, `steps`, `category_id`, `image_url`)。
  - 處理邏輯：呼叫 `Recipe` Model 的建立方法，自動產生 `share_token`。
  - 輸出：重導向至 `/` 或 `/recipe/<id>`。
  - 錯誤處理：若必填欄位短缺，顯示錯誤訊息並重新渲染 `templates/recipe/create.html`。
- **更新食譜 (POST /recipe/<id>/update)**:
  - 輸入：表單欄位 (`title`, `ingredients`, `steps`, `category_id`, `image_url`)。
  - 處理邏輯：更新對應 `id` 的 `Recipe` 記錄。
  - 輸出：重導向至 `/recipe/<id>`。
- **刪除食譜 (POST /recipe/<id>/delete)**:
  - 處理邏輯：刪除對應 `id` 的紀錄。
  - 輸出：重導向至 `/`。

### Search 模組 (`/search`)
- **搜尋食譜 (GET /search)**:
  - 輸入：URL 參數 `?q=關鍵字`。
  - 處理邏輯：在 `Recipe` Model 內以 `title` 進行模糊搜尋。
  - 輸出：渲染 `templates/search/results.html`。

### Category 模組 (`/category`)
- **新增分類 (POST /category)**:
  - 輸入：表單欄位 `name`。
  - 處理邏輯：如果 `name` 已存在，回應錯誤訊息。否則建立分類紀錄。
  - 輸出：重導向至 `/category`。

### Share 模組 (`/share`)
- **唯讀分享頁 (GET /share/<share_token>)**:
  - 輸入：URL 參數 `share_token`。
  - 處理邏輯：根據 token 從 `Recipe` Model 中讀取對應食譜。
  - 輸出：渲染 `templates/recipe/share.html`，且頁面內不包含任何編輯或刪除的按鈕。
  - 錯誤處理：若無此 token 則回傳 404 頁面。

## 3. Jinja2 模板清單

- `templates/base.html` (所有模板的基礎，包含導覽列)
- `templates/index.html` (繼承 base.html，首頁清單/分類清單)
- `templates/recipe/create.html` (繼承 base.html)
- `templates/recipe/edit.html` (繼承 base.html)
- `templates/recipe/detail.html` (繼承 base.html)
- `templates/recipe/share.html` (繼承 base.html)
- `templates/search/results.html` (繼承 base.html)
- `templates/category/list.html` (繼承 base.html)

## 4. 路由骨架程式碼
請參考 `app/routes/` 資料夾下各個模組。
