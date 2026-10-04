# -*- coding: utf-8 -*-
"""Very small translation table (English / Russian)."""

_LANG = ["en"]

STRINGS = {
    "app_title": ("Enigma Cube", "Enigma Cube"),
    "about": ("About Enigma Cube", "О программе"),
    "about_text": ("Speedcubing timer with WCA scrambles for 14 events, inspection, "
                   "sessions and statistics. Works fully offline.",
                   "Таймер для спидкубинга: скрамблы WCA для 14 дисциплин, инспекция, "
                   "сессии и статистика. Работает полностью офлайн."),
    "minimal_mode": ("Minimal mode", "Минимальный режим"),
    "tab_progress": ("Progress", "Прогресс"),
    "tab_distribution": ("Distribution", "Распределение"),
    "dist_need": ("Distribution appears after %d more solves",
                  "Распределение появится ещё через %d сборок"),
    "current": ("Current", "Текущее"),
    "best": ("Best", "Лучшее"),
    "single": ("single", "сингл"),
    "solves": ("Solves", "Сборок"),
    "mean": ("Mean", "Среднее"),
    "sd": ("σ", "σ"),
    "time": ("Time", "Время"),
    "session": ("Session", "Сессия"),
    "new_session": ("New session…", "Новая сессия…"),
    "rename_session": ("Rename session…", "Переименовать…"),
    "delete_session": ("Delete session", "Удалить сессию"),
    "clear_session": ("Clear all solves", "Очистить все сборки"),
    "import_cstimer": ("Import from csTimer…", "Импорт из csTimer…"),
    "export_csv": ("Export session to CSV…", "Экспорт сессии в CSV…"),
    "manual_entry": ("Enter time manually…", "Ввести время вручную…"),
    "settings": ("Settings", "Настройки"),
    "session_name": ("Session name:", "Название сессии:"),
    "confirm_delete_session": ("Delete session “%s” with %d solves?",
                               "Удалить сессию «%s» (%d сборок)?"),
    "confirm_clear": ("Delete all %d solves from this session?",
                      "Удалить все %d сборок из этой сессии?"),
    "confirm_delete_solve": ("Delete solve %s?", "Удалить сборку %s?"),
    "next_scramble": ("New scramble (N)", "Новый скрамбл (N)"),
    "copy_scramble": ("Copy scramble", "Копировать скрамбл"),
    "copied": ("Copied", "Скопировано"),
    "ready_hint": ("Hold SPACE, release to start", "Зажми ПРОБЕЛ и отпусти для старта"),
    "inspect_hint": ("Press SPACE to start inspection", "Нажми ПРОБЕЛ, чтобы начать инспекцию"),
    "inspection": ("inspection", "инспекция"),
    "solving": ("solving…", "сборка…"),
    "preview_na": ("No preview for this puzzle", "Нет превью для этой головоломки"),
    "not_enough_data": ("Chart appears after 2 solves", "График появится после 2 сборок"),
    "new_pb": ("New PB %s: %s!", "Новый рекорд %s: %s!"),
    "ok": ("OK", "OK"),
    "plus2": ("+2", "+2"),
    "dnf": ("DNF", "DNF"),
    "delete": ("Delete", "Удалить"),
    "comment": ("Comment", "Комментарий"),
    "comment_prompt": ("Comment:", "Комментарий:"),
    "copy": ("Copy", "Копировать"),
    "close": ("Close", "Закрыть"),
    "copy_scramble_menu": ("Copy scramble", "Копировать скрамбл"),
    "solve_n": ("Solve #%d", "Сборка №%d"),
    "scramble": ("Scramble", "Скрамбл"),
    "date": ("Date", "Дата"),
    "enter_time": ("Time (e.g. 12.34, 1:05.20, 1234, DNF, 14.00+):",
                   "Время (например 12.34, 1:05.20, 1234, DNF, 14.00+):"),
    "bad_time": ("Could not read that time.", "Не удалось распознать время."),
    "imported": ("Imported %d sessions, %d solves.", "Импортировано сессий: %d, сборок: %d."),
    "import_failed": ("Import failed: %s", "Ошибка импорта: %s"),
    "exported": ("Saved to %s", "Сохранено в %s"),
    # settings dialog
    "s_inspection": ("15-second WCA inspection", "Инспекция WCA 15 секунд"),
    "s_alerts": ("Beep at 8 s and 12 s of inspection", "Сигнал на 8 и 12 секунде инспекции"),
    "s_hold": ("Hold time before start", "Удержание перед стартом"),
    "s_update": ("Timer while solving", "Таймер во время сборки"),
    "u_full": ("Show everything", "Показывать полностью"),
    "u_tenths": ("Tenths only", "Только десятые"),
    "u_seconds": ("Seconds only", "Только секунды"),
    "u_hidden": ("Hide (shows “solving…”)", "Скрывать («сборка…»)"),
    "s_decimals": ("Decimal places", "Знаков после запятой"),
    "s_focus": ("Focus mode: hide everything while solving",
                "Режим фокуса: скрывать всё во время сборки"),
    "s_preview": ("Show scramble preview", "Показывать превью скрамбла"),
    "s_chart": ("Show progress chart", "Показывать график прогресса"),
    "s_language": ("Language", "Язык"),
    "lang_auto": ("System language", "Как в системе"),
    "restart_needed": ("Language will change after restart.",
                       "Язык сменится после перезапуска."),
    "shortcuts": ("Shortcuts", "Горячие клавиши"),
    "shortcuts_text": (
        "Space — hold & release to start, any key stops\n"
        "Esc — cancel inspection\n"
        "Ctrl+1 / Ctrl+2 / Ctrl+3 — last solve OK / +2 / DNF\n"
        "Ctrl+Z — delete last solve\n"
        "N — new scramble\n"
        "Ctrl+E — enter time manually",
        "Пробел — зажать и отпустить для старта, любая клавиша — стоп\n"
        "Esc — отменить инспекцию\n"
        "Ctrl+1 / Ctrl+2 / Ctrl+3 — последняя сборка OK / +2 / DNF\n"
        "Ctrl+Z — удалить последнюю сборку\n"
        "N — новый скрамбл\n"
        "Ctrl+E — ввести время вручную"),
    "chart_single": ("single", "сингл"),
    "average_of": ("Average", "Среднее"),
}


def set_language(lang):
    _LANG[0] = "ru" if lang == "ru" else "en"


def tr(key):
    pair = STRINGS.get(key)
    if pair is None:
        return key
    return pair[1] if _LANG[0] == "ru" else pair[0]
