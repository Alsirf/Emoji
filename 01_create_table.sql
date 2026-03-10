-- Назначение: Создание таблицы для хранения эмодзи
-- Выполнить: в старой и новой БД
-- 
-- ЗАМЕНИТЬ: PTD.emojis на нужное имя таблицы (schema.table_name)

CREATE TABLE PTD.emojis  -- замените на schema.table_name
(
    `id` UInt64 COMMENT 'Номер строки',
    `symbol` String COMMENT 'Эмодзи',
    `code` String COMMENT 'Кодовые точки (U+XXXX)',
    `description` String COMMENT 'Описание',
    `category` String COMMENT 'Категория',
    `length` UInt64 COMMENT 'Количество кодовых точек'
) 
ENGINE = MergeTree()
ORDER BY (id);

-- После создания можно проверить:
-- DESCRIBE TABLE PTD.emojis;
