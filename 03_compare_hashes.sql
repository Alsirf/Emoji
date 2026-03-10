WITH old_ch AS (
    SELECT hex(sipHash128 ([
        coalesce(id::Nullable(String), 'NULL'),
        coalesce(symbol::Nullable(String), 'NULL'),
        coalesce(code::Nullable(String), 'NULL'),
        coalesce(description::Nullable(String), 'NULL'),
        coalesce(category::Nullable(String), 'NULL'),
        coalesce(length::Nullable(String), 'NULL')
    ])) AS hash
    FROM PTD.emojis  -- ⚠️ замените на имя таблицы в старой БД
),
new_ch AS (
    SELECT hex(sipHash128 ([
        coalesce(id::Nullable(String), 'NULL'),
        coalesce(symbol::Nullable(String), 'NULL'),
        coalesce(code::Nullable(String), 'NULL'),
        coalesce(description::Nullable(String), 'NULL'),
        coalesce(category::Nullable(String), 'NULL'),
        coalesce(length::Nullable(String), 'NULL')
    ])) AS hash
    FROM remoteSecure(
       'example-host0154.ru:1111',      -- ⚠️ замените на хост:порт новой БД
        PTD.emojis,       -- ⚠️ замените на имя таблицы в новой БД
        'login',       -- ⚠️ замените на логин к новой БД
        'password'        -- ⚠️ замените на пароль к новой БД
    )
)
SELECT
    sum(CASE WHEN old_ch.hash IS NOT NULL THEN 1 ELSE 0 END) as records_in_old,
    sum(CASE WHEN new_ch.hash IS NOT NULL THEN 1 ELSE 0 END) as records_in_new,
    sum(CASE WHEN old_ch.hash IS NULL THEN 1 ELSE 0 END) as only_in_new,
    sum(CASE WHEN new_ch.hash IS NULL THEN 1 ELSE 0 END) as only_in_old
FROM old_ch
FULL JOIN new_ch ON old_ch.hash = new_ch.hash;

