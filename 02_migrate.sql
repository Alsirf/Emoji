-- Назначение: Миграция данных из старой БД в новую
-- Выполнить: в старой БД

-- 1. Миграция данных
INSERT INTO TABLE FUNCTION 
remoteSecure(
        'example-host0154.ru:1111',      -- ⚠️ замените на хост:порт новой БД
        PTD.emojis,       -- ⚠️ замените на имя таблицы в новой БД
        'login',       -- ⚠️ замените на логин к новой БД
        'password'        -- ⚠️ замените на пароль к новой БД
    )
SELECT id, symbol, code, description, category, length
FROM [database.table]          -- название таблицы в старой БД
SETTINGS max_threads = 4;
