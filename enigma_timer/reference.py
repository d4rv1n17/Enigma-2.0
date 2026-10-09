# -*- coding: utf-8 -*-
"""Notation reference for every WCA puzzle (English / Russian HTML).

Images: <img src="move:<puzzle>:<moves>"> shows the puzzle after <moves>
applied to a solved puzzle (rendered by the Training views)."""

PUZZLES = [
    ("333", ("3x3 cube", "Куб 3x3")),
    ("222", ("2x2 cube", "Куб 2x2")),
    ("444", ("4x4–7x7 cubes", "Кубы 4x4–7x7")),
    ("pyram", ("Pyraminx", "Пирамидка")),
    ("skewb", ("Skewb", "Скьюб")),
    ("minx", ("Megaminx", "Мегаминкс")),
    ("sq1", ("Square-1", "Square-1")),
    ("clock", ("Clock", "Clock")),
]


def _moves(puzzle, moves, labels, width=86):
    cells = "".join('<td align="center"><img src="move:%s:%s" width="%d"></td>'
                    % (puzzle, m, width) for m in moves)
    caps = "".join('<td align="center"><b>%s</b></td>' % lab for lab in labels)
    return '<table cellspacing="8"><tr>%s</tr><tr>%s</tr></table>' % (cells, caps)


def html(puzzle, lang):
    ru = lang == "ru"
    f = _RU if ru else _EN
    return f.get(puzzle, "")


_EN = {}
_RU = {}

_EN["333"] = """<h2>3x3 notation</h2>
<p>Hold the cube with one face towards you. A letter turns that face <b>90&deg; clockwise as
seen looking straight at it</b>. <b>'</b> = counter-clockwise, <b>2</b> = 180&deg;.</p>
""" + _moves("333", ["R", "L", "U", "D", "F", "B"], ["R", "L", "U", "D", "F", "B"], 78) + """
<h3>Wide moves, slices and rotations</h3>
""" + _moves("333", ["r", "M", "E", "S", "x", "y"], ["r = Rw", "M", "E", "S", "x", "y"], 78) + """
<ul>
<li><b>r</b> (or <b>Rw</b>): right face plus the middle layer. Same for l, u, d, f, b.</li>
<li><b>M</b> follows L, <b>E</b> follows D, <b>S</b> follows F.</li>
<li><b>x, y, z</b> rotate the whole cube like R, U and F.</li>
<li>Brackets <b>( )</b> only group moves; they change nothing.</li>
</ul>"""

_RU["333"] = """<h2>Нотация 3x3</h2>
<p>Держи куб одной гранью к себе. Буква поворачивает эту грань <b>на 90&deg; по часовой
стрелке, если смотреть прямо на неё</b>. <b>'</b> — против часовой, <b>2</b> — на 180&deg;.</p>
""" + _moves("333", ["R", "L", "U", "D", "F", "B"], ["R", "L", "U", "D", "F", "B"], 78) + """
<h3>Широкие ходы, слайсы и повороты</h3>
""" + _moves("333", ["r", "M", "E", "S", "x", "y"], ["r = Rw", "M", "E", "S", "x", "y"], 78) + """
<ul>
<li><b>r</b> (или <b>Rw</b>): правая грань вместе со средним слоем. Так же l, u, d, f, b.</li>
<li><b>M</b> крутится как L, <b>E</b> — как D, <b>S</b> — как F.</li>
<li><b>x, y, z</b> — поворот всего куба как R, U и F.</li>
<li>Скобки <b>( )</b> только группируют ходы и ничего не меняют.</li>
</ul>"""

_EN["222"] = """<h2>2x2 notation</h2>
<p>Exactly like the 3x3: R, U, F, L, D, B with ' and 2. WCA scrambles use only R, U and F.</p>
""" + _moves("222", ["R", "U", "F"], ["R", "U", "F"], 86)
_RU["222"] = """<h2>Нотация 2x2</h2>
<p>Точно как на 3x3: R, U, F, L, D, B с ' и 2. Скрамблы WCA используют только R, U и F.</p>
""" + _moves("222", ["R", "U", "F"], ["R", "U", "F"], 86)

_EN["444"] = """<h2>Big cube notation (4x4–7x7)</h2>
""" + _moves("444", ["R", "Rw", "2R", "3Rw"], ["R", "Rw", "2R", "3Rw"], 86) + """
<ul>
<li><b>R</b>: only the outer layer.</li>
<li><b>Rw</b> (or <b>r</b> on a 4x4): the two outer layers together.</li>
<li><b>3Rw</b>: the three outer layers together (5x5 and bigger).</li>
<li><b>2R</b>: only the second layer (an inner slice).</li>
<li>Same for U, F, L, D, B: <b>Uw</b>, <b>3Fw</b>, <b>2U</b>…</li>
</ul>"""
_RU["444"] = """<h2>Нотация больших кубов (4x4–7x7)</h2>
""" + _moves("444", ["R", "Rw", "2R", "3Rw"], ["R", "Rw", "2R", "3Rw"], 86) + """
<ul>
<li><b>R</b>: только внешний слой.</li>
<li><b>Rw</b> (или <b>r</b> на 4x4): два внешних слоя вместе.</li>
<li><b>3Rw</b>: три внешних слоя вместе (5x5 и больше).</li>
<li><b>2R</b>: только второй слой (внутренний слайс).</li>
<li>Так же для U, F, L, D, B: <b>Uw</b>, <b>3Fw</b>, <b>2U</b>…</li>
</ul>"""

_EN["pyram"] = """<h2>Pyraminx notation (WCA)</h2>
<p>Hold the Pyraminx with one face towards you and a corner up. Each letter turns two layers
around a corner <b>120&deg; clockwise, looking at that corner</b>.</p>
""" + _moves("pyram", ["U", "L", "R", "B"], ["U", "L", "R", "B"], 96) + """
<ul>
<li><b>U, L, R, B</b>: the top, left, right and back corner (two layers).</li>
<li><b>u, l, r, b</b>: only the small tip of that corner.</li>
<li><b>'</b> = counter-clockwise.</li>
</ul>"""
_RU["pyram"] = """<h2>Нотация Пирамидки (WCA)</h2>
<p>Держи Пирамидку гранью к себе и вершиной вверх. Буква поворачивает два слоя вокруг
вершины <b>на 120&deg; по часовой стрелке, если смотреть на эту вершину</b>.</p>
""" + _moves("pyram", ["U", "L", "R", "B"], ["U", "L", "R", "B"], 96) + """
<ul>
<li><b>U, L, R, B</b>: верхняя, левая, правая и задняя вершина (два слоя).</li>
<li><b>u, l, r, b</b>: только маленький кончик этой вершины.</li>
<li><b>'</b> — против часовой стрелки.</li>
</ul>"""

_EN["skewb"] = """<h2>Skewb notation (WCA)</h2>
<p>Every move turns half of the puzzle <b>120&deg; clockwise around a corner</b>, looking at it.
With white on top and green in front:</p>
""" + _moves("skewb", ["R", "U", "L", "B"], ["R", "U", "L", "B"], 96) + """
<ul>
<li><b>R</b>: the bottom-back-right corner (DBR).</li>
<li><b>U</b>: the top-back-left corner (UBL).</li>
<li><b>L</b>: the bottom-front-left corner (DFL).</li>
<li><b>B</b>: the bottom-back-left corner (DBL).</li>
</ul>
<p>Many tutorials use "Sarah's notation" instead (other corners). All Skewb algorithms in
Enigma Cube use the WCA notation above.</p>"""
_RU["skewb"] = """<h2>Нотация Скьюба (WCA)</h2>
<p>Каждый ход поворачивает половину головоломки <b>на 120&deg; по часовой стрелке вокруг
угла</b>, если смотреть на него. Белый сверху, зелёный спереди:</p>
""" + _moves("skewb", ["R", "U", "L", "B"], ["R", "U", "L", "B"], 96) + """
<ul>
<li><b>R</b>: нижний задний правый угол (DBR).</li>
<li><b>U</b>: верхний задний левый угол (UBL).</li>
<li><b>L</b>: нижний передний левый угол (DFL).</li>
<li><b>B</b>: нижний задний левый угол (DBL).</li>
</ul>
<p>Во многих уроках используют «нотацию Сары» (с другими углами). Все алгоритмы Скьюба
в Enigma Cube записаны в нотации WCA выше.</p>"""

_EN["minx"] = """<h2>Megaminx notation</h2>
<p><b>Scrambles (Pochmann):</b> <b>R++</b> / <b>R--</b> turn everything except the left face
two fifths (144&deg;) up or down; <b>D++</b> / <b>D--</b> do the same for everything except the
top; <b>U</b> / <b>U'</b> turn the top face one fifth.</p>
<p><b>Algorithms:</b> like a 3x3 — <b>R, U, F, L</b> turn a face 72&deg; clockwise, <b>U2</b> =
144&deg;, <b>U2'</b> = 144&deg; counter-clockwise. <b>BR</b>, <b>BL</b> are the back-right and
back-left faces.</p>"""
_RU["minx"] = """<h2>Нотация Мегаминкса</h2>
<p><b>Скрамблы (Похман):</b> <b>R++</b> / <b>R--</b> поворачивают всё, кроме левой грани, на
две пятых (144&deg;) вверх или вниз; <b>D++</b> / <b>D--</b> — всё, кроме верха; <b>U</b> /
<b>U'</b> — верхнюю грань на одну пятую.</p>
<p><b>Алгоритмы:</b> как на 3x3 — <b>R, U, F, L</b> поворачивают грань на 72&deg; по часовой,
<b>U2</b> — на 144&deg;, <b>U2'</b> — на 144&deg; против часовой. <b>BR</b>, <b>BL</b> — задняя
правая и задняя левая грани.</p>"""

_EN["sq1"] = """<h2>Square-1 notation</h2>
<p><b>(x, y)</b>: turn the top layer x steps and the bottom layer y steps of 30&deg; each,
clockwise as seen from that layer; negative numbers turn the other way.
<b>/</b> is the slice: the right half turns 180&deg;.</p>
""" + _moves("sq1", ["", "(1,0) /", "(0,-1) /"], ["solved", "(1,0) /", "(0,-1) /"], 150) + """
<p>Edges are 30&deg; wedges, corners are 60&deg; kites. The dashed line shows where the slice
cuts.</p>"""
_RU["sq1"] = """<h2>Нотация Square-1</h2>
<p><b>(x, y)</b>: повернуть верхний слой на x шагов и нижний на y шагов по 30&deg;, по часовой
стрелке, если смотреть на этот слой; отрицательные числа — в другую сторону.
<b>/</b> — слайс: правая половина поворачивается на 180&deg;.</p>
""" + _moves("sq1", ["", "(1,0) /", "(0,-1) /"], ["собран", "(1,0) /", "(0,-1) /"], 150) + """
<p>Рёбра — клинья по 30&deg;, углы — «воздушные змеи» по 60&deg;. Пунктир показывает, где
проходит слайс.</p>"""

_EN["clock"] = """<h2>Clock notation (WCA)</h2>
<ul>
<li><b>UR, DR, DL, UL</b>: only that pin is up; turn its dial.</li>
<li><b>U, R, D, L</b>: the two pins on that side are up.</li>
<li><b>ALL</b>: all four pins are up.</li>
<li><b>4+</b> / <b>2-</b>: turn the dial 4 hours clockwise / 2 hours counter-clockwise.</li>
<li><b>y2</b>: turn the clock over (left and right stay in place).</li>
</ul>
<p>Example: <b>UR3+</b> — upper-right pin up, turn its dial 3 hours clockwise.</p>"""
_RU["clock"] = """<h2>Нотация Clock (WCA)</h2>
<ul>
<li><b>UR, DR, DL, UL</b>: поднят только этот штырёк; крутишь его колесо.</li>
<li><b>U, R, D, L</b>: подняты два штырька с этой стороны.</li>
<li><b>ALL</b>: подняты все четыре штырька.</li>
<li><b>4+</b> / <b>2-</b>: повернуть колесо на 4 часа по часовой / на 2 часа против.</li>
<li><b>y2</b>: перевернуть часы другой стороной (лево и право остаются на месте).</li>
</ul>
<p>Пример: <b>UR3+</b> — поднят правый верхний штырёк, колесо на 3 часа по часовой.</p>"""
