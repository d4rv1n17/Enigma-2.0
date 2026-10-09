# -*- coding: utf-8 -*-
"""Very small translation table (English / Russian)."""

_LANG = ["en"]

STRINGS = {
    "app_title": ("Enigma Cube", "Enigma Cube"),
    "about": ("About Enigma Cube", "О программе"),
    "about_text": ("Speedcubing timer and trainer: WCA scrambles for 14 events, statistics, "
                   "courses for every event, a notation reference and achievements. "
                   "Works fully offline.",
                   "Таймер и тренажёр для спидкубинга: скрамблы WCA для 14 дисциплин, статистика, "
                   "курсы по всем дисциплинам, справочник нотации и достижения. "
                   "Работает полностью офлайн."),
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
    # training
    "nav_timer": ("Timer", "Таймер"),
    "nav_training": ("Training", "Тренировка"),
    "nav_reference": ("Reference", "Справочник"),
    "nav_achievements": ("Achievements", "Достижения"),
    "reference": ("Notation", "Нотация"),
    "achievements": ("Achievements", "Достижения"),
    "ach_summary": ("%d of %d unlocked", "Получено %d из %d"),
    "ach_new": ("Achievement unlocked: %s", "Новое достижение: %s"),
    "ach_many": ("%d achievements unlocked", "Получено достижений: %d"),
    "new_window": ("Open Training in a new window", "Открыть тренировку в новом окне"),
    "pin_window": ("Keep on top of other windows", "Поверх других окон"),
    "path": ("Learning path", "Путь обучения"),
    "next_up": ("Next step", "Следующий шаг"),
    "train": ("Practise", "Тренировать"),
    "train_case": ("Practise this case", "Тренировать этот случай"),
    "lesson": ("Lesson", "Урок"),
    "algorithms": ("Algorithms", "Алгоритмы"),
    "mark_lesson": ("Mark lesson as done", "Урок пройден"),
    "lesson_done": ("Lesson done ✓", "Урок пройден ✓"),
    "learned_of": ("%d of %d learned", "Выучено %d из %d"),
    "due_now": ("%d to review", "%d к повторению"),
    "f_all": ("All", "Все"),
    "f_new": ("New", "Новые"),
    "f_learning": ("Learning", "Учу"),
    "f_learned": ("Learned", "Выучено"),
    "st_new": ("New", "Новый"),
    "st_learning": ("Learning", "Учу"),
    "st_learned": ("Learned", "Выучил"),
    "setup_hint": ("Set up: %s", "Как поставить: %s"),
    "trainer_title": ("Practice · %s", "Тренировка · %s"),
    "back": ("Back", "Назад"),
    "reveal": ("Show algorithm", "Показать алгоритм"),
    "reveal_hint": ("Recognise the case, solve it, then press Space",
                    "Узнай случай, собери его и нажми Пробел"),
    "r_again": ("Forgot  1", "Не помню  1"),
    "r_hard": ("Hard  2", "С трудом  2"),
    "r_good": ("Knew it  3", "Помню  3"),
    "session_stats": ("Reviewed %d · %d to review", "Повторено %d · к повторению %d"),
    "select_case": ("Pick a case to see its algorithm", "Выбери случай, чтобы увидеть алгоритм"),
    "empty_filter": ("Nothing here yet", "Здесь пока пусто"),
    "average_of": ("Average", "Среднее"),
}


def lang():
    return _LANG[0]


def pick(pair):
    """Choose the right text from an (en, ru) tuple."""
    if not pair:
        return ""
    return pair[1] if _LANG[0] == "ru" else pair[0]


def set_language(lang):
    _LANG[0] = "ru" if lang == "ru" else "en"


def tr(key):
    pair = STRINGS.get(key)
    if pair is None:
        return key
    return pair[1] if _LANG[0] == "ru" else pair[0]
