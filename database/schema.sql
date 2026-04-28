-- =========================================
-- 食譜收藏夾 Recipe Collection System
-- SQLite Schema
-- =========================================

-- 分類資料表
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    name        TEXT     NOT NULL UNIQUE,
    description TEXT,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 食譜資料表
CREATE TABLE IF NOT EXISTS recipes (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    title        TEXT     NOT NULL,
    ingredients  TEXT     NOT NULL,
    steps        TEXT     NOT NULL,
    image_url    TEXT,
    share_token  TEXT     NOT NULL UNIQUE,
    category_id  INTEGER  REFERENCES categories(id) ON DELETE SET NULL,
    created_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 索引：加速依分類篩選
CREATE INDEX IF NOT EXISTS idx_recipes_category_id
    ON recipes(category_id);

-- 索引：加速分享頁面查詢
CREATE INDEX IF NOT EXISTS idx_recipes_share_token
    ON recipes(share_token);

-- 索引：加速關鍵字搜尋
CREATE INDEX IF NOT EXISTS idx_recipes_title
    ON recipes(title);
