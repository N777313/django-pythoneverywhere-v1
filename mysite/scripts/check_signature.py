import hashlib
import hmac
import urllib.parse

# Поставь сюда твой initData
init_data = "query_id=AAE0HqEqAAAAADQeoSp5MG8c&user=%7B%22id%22%3A715202100%2C%22first_name%22%3A%22D.W.%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22x100777%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FUD_eJxFQ0bYdI44RY-tx_HK-yRQUvlTQml2Wp-9scXM.svg%22%7D&auth_date=1745702277&signature=H9PwZSMPbylPlH5jxzFMJFye44Vq5e1K9gAXQfJSIA4SUS4fwv0khwua_kKnZYWMrqI8BsHfOZeqnTtG2DO7BQ&hash=0406f6db766a246350cfd6090d2a93bdf0862831adc9552fdcffc80559f3c1d6"

# Твой реальный токен сюда
bot_token = "7644595150:AAED5nPSZ87dQJ_1X-9Qk8shQvheU0LVLO4"

# Парсим initData
parsed_data = dict(urllib.parse.parse_qsl(init_data))

# Извлекаем полученный от Telegram хэш
hash_received = parsed_data.pop('hash', '')

# Убираем поле signature (его вообще не трогаем)
parsed_data.pop('signature', None)

# Строим data_check_string
data_check_string = '\n'.join(
    f'{k}={v}' for k, v in sorted(parsed_data.items())
)

# Строим секретный ключ
secret_key = hashlib.sha256(bot_token.encode()).digest()

# Вычисляем свой HMAC
hmac_string = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

# Вывод
print("Data Check String:\n", data_check_string)
print("Generated HMAC String:\n", hmac_string)
print("Received Hash:\n", hash_received)

# Сравнение
if hmac_string == hash_received:
    print("✅ Подпись верная! Всё отлично.")
else:
    print("❌ Подпись НЕ совпала! Есть ошибка.")
