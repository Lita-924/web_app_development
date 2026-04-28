# 流程圖文件：食譜收藏夾 (Recipe Collection System)

> 根據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md` 產出，使用 Mermaid 語法繪製。

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([🌐 使用者開啟網站]) --> Home[首頁\n食譜列表]

    Home --> Search[🔍 輸入關鍵字搜尋]
    Search --> SearchResult[搜尋結果頁]
    SearchResult --> Detail

    Home --> FilterCat[篩選分類]
    FilterCat --> Home

    Home --> Detail[📄 食譜詳情頁]

    Home --> NewBtn[點擊「新增食譜」]
    NewBtn --> CreateForm[填寫食譜表單\n標題 / 食材 / 步驟 / 分類]
    CreateForm --> Validate{表單驗證}
    Validate -->|❌ 有誤| CreateForm
    Validate -->|✅ 通過| SaveRecipe[(儲存到資料庫)]
    SaveRecipe --> Home

    Detail --> EditBtn[點擊「編輯」]
    EditBtn --> EditForm[修改食譜表單]
    EditForm --> EditValidate{表單驗證}
    EditValidate -->|❌ 有誤| EditForm
    EditValidate -->|✅ 通過| UpdateRecipe[(更新資料庫)]
    UpdateRecipe --> Detail

    Detail --> DeleteBtn[點擊「刪除」]
    DeleteBtn --> Confirm{確認刪除？}
    Confirm -->|取消| Detail
    Confirm -->|確認| DeleteRecipe[(從資料庫刪除)]
    DeleteRecipe --> Home

    Detail --> ShareBtn[點擊「分享」]
    ShareBtn --> SharePage[📤 唯讀分享頁\n/share/uuid]
    SharePage --> CopyLink[複製分享連結]

    Home --> CatBtn[點擊「管理分類」]
    CatBtn --> CatList[分類列表]
    CatList --> NewCat[新增分類]
    NewCat --> CatList
```

---

## 2. 系統序列圖（Sequence Diagram）

描述每個主要操作在系統內部（瀏覽器 → Flask → Model → SQLite）的完整資料流。

### 2.1 新增食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「新增食譜」
    Browser->>Flask: GET /recipes/create
    Flask-->>Browser: 回傳 create.html 表單

    User->>Browser: 填寫標題、食材、步驟、選擇分類，送出
    Browser->>Flask: POST /recipes/create
    Flask->>Flask: 驗證表單資料（必填欄位、XSS 過濾）
    alt 驗證失敗
        Flask-->>Browser: 回傳表單頁 + 錯誤提示
    else 驗證通過
        Flask->>Model: Recipe.create(data)
        Model->>DB: INSERT INTO recipes (...)
        DB-->>Model: 回傳新建 recipe_id
        Model-->>Flask: 回傳 Recipe 物件
        Flask-->>Browser: 302 重導向至首頁
    end
```

### 2.2 搜尋食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 輸入關鍵字並按下搜尋
    Browser->>Flask: GET /search?q=關鍵字
    Flask->>Model: Recipe.search(keyword)
    Model->>DB: SELECT * FROM recipes WHERE title LIKE '%keyword%'
    DB-->>Model: 回傳符合的食譜清單
    Model-->>Flask: 回傳 Recipe 列表
    Flask-->>Browser: 回傳 search/results.html（含結果）
    Browser-->>User: 顯示搜尋結果
```

### 2.3 編輯食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「編輯」按鈕
    Browser->>Flask: GET /recipes/<id>/edit
    Flask->>Model: Recipe.get_by_id(id)
    Model->>DB: SELECT * FROM recipes WHERE id = ?
    DB-->>Model: 回傳食譜資料
    Model-->>Flask: 回傳 Recipe 物件
    Flask-->>Browser: 回傳 recipe/edit.html（預填資料）

    User->>Browser: 修改內容並送出
    Browser->>Flask: POST /recipes/<id>/edit
    Flask->>Flask: 驗證資料
    Flask->>Model: Recipe.update(id, data)
    Model->>DB: UPDATE recipes SET ... WHERE id = ?
    DB-->>Model: 更新成功
    Model-->>Flask: 成功
    Flask-->>Browser: 302 重導向至詳情頁
```

### 2.4 刪除食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」並確認
    Browser->>Flask: POST /recipes/<id>/delete
    Flask->>Model: Recipe.delete(id)
    Model->>DB: DELETE FROM recipes WHERE id = ?
    DB-->>Model: 刪除成功
    Model-->>Flask: 成功
    Flask-->>Browser: 302 重導向至首頁
```

### 2.5 分享食譜（唯讀連結）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「分享」按鈕
    Browser->>Flask: GET /share/<share_token>
    Flask->>Model: Recipe.get_by_token(share_token)
    Model->>DB: SELECT * FROM recipes WHERE share_token = ?
    DB-->>Model: 回傳食譜資料
    Model-->>Flask: 回傳 Recipe 物件
    Flask-->>Browser: 回傳 recipe/share.html（唯讀模式）
    Browser-->>User: 顯示唯讀食譜頁，可複製連結
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 首頁 / 食譜列表 | `/` | GET | 顯示所有食譜，支援分類篩選 |
| 新增食譜（表單頁） | `/recipes/create` | GET | 顯示新增食譜表單 |
| 新增食譜（送出） | `/recipes/create` | POST | 接收表單資料，寫入資料庫 |
| 食譜詳情 | `/recipes/<id>` | GET | 顯示單筆食譜完整內容 |
| 編輯食譜（表單頁） | `/recipes/<id>/edit` | GET | 顯示預填資料的編輯表單 |
| 編輯食譜（送出） | `/recipes/<id>/edit` | POST | 接收修改資料，更新資料庫 |
| 刪除食譜 | `/recipes/<id>/delete` | POST | 刪除指定食譜 |
| 搜尋食譜 | `/search` | GET | 接收 `?q=` 參數，回傳搜尋結果 |
| 分享食譜（唯讀） | `/share/<share_token>` | GET | 以 UUID token 顯示唯讀食譜頁 |
| 分類列表 | `/categories` | GET | 顯示所有分類 |
| 新增分類（表單頁） | `/categories/create` | GET | 顯示新增分類表單 |
| 新增分類（送出） | `/categories/create` | POST | 寫入新分類到資料庫 |

---

*文件版本：v1.0 — 2026-04-28*
