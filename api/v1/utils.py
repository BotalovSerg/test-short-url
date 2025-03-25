def get_short_url(url: str) -> str:
    """
    Генерирует сокращенный идентификатор на основе переданного URL.

    Логика генерации:
        - Удаляется завершающий слэш (`/`) из URL.
        - Идентификатор формируется как комбинация:
            1. Первый символ URL.
            2. Длина URL (количество символов).
            3. Последний символ URL.

    Параметры:
        url (str): Оригинальный URL, для которого нужно сгенерировать идентификатор.

    Возвращаемое значение:
        str: Сокращенный идентификатор в формате "<первый_символ><длина><последний_символ>".

    Пример:
        Вход: "https://example.com"
        Выход: "h18m"

        Вход: "https://test.com/"
        Выход: "h17m"
    """
    cut_url = url.rstrip("/")
    return cut_url[0] + str(len(cut_url)) + cut_url[-1]
