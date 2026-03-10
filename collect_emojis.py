import csv
import os
import urllib.request
import ssl
import unicodedata

# --- Игнорируем SSL ошибки (для корпоративных сетей) ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- Настройки (можно менять) ---
BASE_URL = "https://unicode.org/Public/emoji/latest/"
FILES = [
    "emoji-test.txt",
    "emoji-zwj-sequences.txt",
    "emoji-sequences.txt",
]

# Определяем пути
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "emojis_with_codes.csv")


def hex_to_emoji(hex_codes):
    """Преобразует hex-коды в символ эмодзи"""
    try:
        parts = hex_codes.strip().split()
        chars = ''.join(chr(int(h, 16)) for h in parts if h.strip())
        codepoints = ' '.join(f'U+{h.upper()}' for h in parts)
        return chars, codepoints, len(parts)
    except Exception:
        return None, None, 0


def get_description(char):
    """Получает описание символа из Unicode"""
    try:
        return unicodedata.name(char).title()
    except ValueError:
        return "Unknown Character"


def get_category(first_ord):
    """Определяет категорию эмодзи по кодовой точке"""
    o = first_ord
    if 0x1F600 <= o <= 0x1F64F:
        return "Smileys & Emotion"
    elif 0x1F300 <= o <= 0x1F5FF:
        return "Symbols & Objects"
    elif 0x1F680 <= o <= 0x1F6FF:
        return "Travel & Places"
    elif 0x1F900 <= o <= 0x1F9FF:
        return "People & Body"
    elif 0x1F1E6 <= o <= 0x1F1FF:
        return "Flags"
    elif 0x2600 <= o <= 0x26FF or 0x2700 <= o <= 0x27BF:
        return "Symbols"
    elif 0x1F380 <= o <= 0x1F3FF:
        return "Activities & Gestures"
    else:
        return "Other"


def main():
    """Основная функция сбора данных"""
    print("🚀 Сбор эмодзи с Unicode.org...")
    
    emojis_data = []
    seen_symbols = set()

    for filename in FILES:
        url = f"{BASE_URL}{filename}"
        try:
            response = urllib.request.urlopen(url, timeout=15)
            data = response.read().decode('utf-8')
        except Exception as e:
            print(f"  ⚠ Ошибка загрузки {filename}: {e}")
            continue

        for line in data.splitlines():
            line = line.strip()
            if not line or line.startswith('#') or ';' not in line:
                continue
                
            body = line.split('#')[0].strip()
            hex_part, status_part = body.split(';', 1)
            status = status_part.strip()
            
            # Берём только fully-qualified эмодзи
            if 'fully-qualified' not in status and 'emoji' not in status:
                continue

            symbol, code, length = hex_to_emoji(hex_part)
            if not symbol or symbol in seen_symbols:
                continue
                
            seen_symbols.add(symbol)
            description = get_description(symbol[0])
            category = get_category(ord(symbol[0]))
            
            emojis_data.append({
                'symbol': symbol,
                'code': code,
                'description': description,
                'category': category,
                'length': length
            })

    print(f"📊 Найдено эмодзи: {len(emojis_data)}")

    # Создаём директорию и сохраняем CSV
    os.makedirs(DATA_DIR, exist_ok=True)
    
    fieldnames = ['id', 'symbol', 'code', 'description', 'category', 'length']
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, item in enumerate(emojis_data, start=1):
            writer.writerow({
                'id': idx,
                'symbol': item['symbol'],
                'code': item['code'],
                'description': item['description'],
                'category': item['category'],
                'length': item['length']
            })

    print(f"CSV сохранён: {CSV_PATH}")


if __name__ == "__main__":
    main()
