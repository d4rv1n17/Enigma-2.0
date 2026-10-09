# -*- coding: utf-8 -*-
"""Lesson texts for the learning path (simple HTML, English and Russian).

Images are referenced as <img src="move:R"> (the cube after that move) and
<img src="case:b-cross"> (an algorithm case); the Training view renders them.
"""

NOTATION = {
    "en": """
<h2>Reading algorithms</h2>
<p>Hold the cube with one face towards you. Every letter is a turn of one face,
<b>clockwise as if you were looking straight at that face</b>.</p>
<table cellspacing="10">
<tr><td><img src="move:R" width="88"></td><td><img src="move:U" width="88"></td>
<td><img src="move:F" width="88"></td></tr>
<tr><td align="center"><b>R</b> right</td><td align="center"><b>U</b> up (top)</td>
<td align="center"><b>F</b> front</td></tr>
<tr><td><img src="move:L" width="88"></td><td><img src="move:D" width="88"></td>
<td><img src="move:B" width="88"></td></tr>
<tr><td align="center"><b>L</b> left</td><td align="center"><b>D</b> down (bottom)</td>
<td align="center"><b>B</b> back</td></tr>
</table>
<h3>Modifiers</h3>
<ul>
<li><b>R'</b> (R prime): turn counter-clockwise.</li>
<li><b>R2</b>: turn twice (180&deg;); the direction does not matter.</li>
<li><b>r</b> or <b>Rw</b>: turn the right face together with the middle layer.</li>
<li><b>M</b>: the middle layer between L and R, in the same direction as L.
    <b>E</b> follows D, <b>S</b> follows F.</li>
<li><b>x, y, z</b>: rotate the whole cube like R, U and F.</li>
</ul>
<h3>Tips</h3>
<ul>
<li>Brackets like <b>(R U R' U')</b> only group moves to make them easier to remember.</li>
<li>R U R' U' is so common it has a nickname: the <b>sexy move</b>.</li>
<li>Learn finger tricks early: turn R and U with your fingers, not your whole wrist.</li>
</ul>
""",
    "ru": """
<h2>Как читать алгоритмы</h2>
<p>Держи куб одной гранью к себе. Каждая буква — поворот одной грани
<b>по часовой стрелке, если смотреть прямо на эту грань</b>.</p>
<table cellspacing="10">
<tr><td><img src="move:R" width="88"></td><td><img src="move:U" width="88"></td>
<td><img src="move:F" width="88"></td></tr>
<tr><td align="center"><b>R</b> правая</td><td align="center"><b>U</b> верхняя</td>
<td align="center"><b>F</b> передняя</td></tr>
<tr><td><img src="move:L" width="88"></td><td><img src="move:D" width="88"></td>
<td><img src="move:B" width="88"></td></tr>
<tr><td align="center"><b>L</b> левая</td><td align="center"><b>D</b> нижняя</td>
<td align="center"><b>B</b> задняя</td></tr>
</table>
<h3>Обозначения</h3>
<ul>
<li><b>R'</b> («R штрих»): поворот против часовой стрелки.</li>
<li><b>R2</b>: два поворота (180&deg;), направление не важно.</li>
<li><b>r</b> или <b>Rw</b>: правая грань вместе со средним слоем.</li>
<li><b>M</b>: средний слой между L и R, крутится как L.
    <b>E</b> — как D, <b>S</b> — как F.</li>
<li><b>x, y, z</b>: поворот всего куба так же, как R, U и F.</li>
</ul>
<h3>Советы</h3>
<ul>
<li>Скобки вроде <b>(R U R' U')</b> только группируют ходы, чтобы их было легче запомнить.</li>
<li>R U R' U' встречается так часто, что у него есть прозвище — <b>«сексуальный ход»</b>.</li>
<li>Сразу учись крутить R и U пальцами, а не всей кистью.</li>
</ul>
""",
}

BEGINNER = {
    "en": """
<h2>Beginner method in 7 steps</h2>
<p>Solve the cube layer by layer. Keep the <b>white</b> face on the bottom
(start with it on top for step 1, then flip the cube) and yellow on top.</p>
<ol>
<li><b>White cross.</b> Make a white plus with edges that also match the side
    centres. No algorithm: move each edge into place by feel.</li>
<li><b>White corners.</b> Put a white corner above its spot at the front-right and
    repeat <b>R U R' U'</b> until it drops into place.</li>
<li><b>Second layer.</b> Find a top edge without yellow, match it with its centre,
    then send it right with <b>U R U' R' U' F' U F</b> or left with
    <b>U' L' U L U F U' F'</b>.</li>
<li><b>Yellow cross.</b> <b>F R U R' U' F'</b>: once from the line, twice from the
    L&nbsp;shape (held at back-left), three times from the dot.</li>
<li><b>Yellow edges.</b> <b>R U R' U R U2 R' U</b> swaps the front and left edges.
    Repeat until all four match their centres.</li>
<li><b>Place the corners.</b> Hold a corner that is already in its spot at
    front-right and do <b>U R U' L' U R' U' L</b> until all corners are in place.</li>
<li><b>Turn the corners.</b> With the cube held still, repeat <b>R' D' R D</b> on the
    front-right corner until its yellow faces up, then turn only U to bring the next
    corner there. The cube looks scrambled in between — that is normal.</li>
</ol>
<p>Practise every algorithm below in the trainer until you can do it without looking.</p>
""",
    "ru": """
<h2>Метод для начинающих за 7 шагов</h2>
<p>Собирай куб слоями. <b>Белая</b> грань внизу (для шага 1 удобнее держать её
сверху, потом переверни куб), жёлтая сверху.</p>
<ol>
<li><b>Белый крест.</b> Собери белый плюс так, чтобы рёбра совпадали и с боковыми
    центрами. Алгоритма нет: ставь каждое ребро на место интуитивно.</li>
<li><b>Белые углы.</b> Поставь белый угол над его местом спереди справа и повторяй
    <b>R U R' U'</b>, пока он не встанет.</li>
<li><b>Второй слой.</b> Найди верхнее ребро без жёлтого цвета, совмести его с центром
    и отправь вправо: <b>U R U' R' U' F' U F</b> или влево:
    <b>U' L' U L U F U' F'</b>.</li>
<li><b>Жёлтый крест.</b> <b>F R U R' U' F'</b>: из линии — 1 раз, из уголка
    (сзади слева) — 2 раза, из точки — 3 раза.</li>
<li><b>Жёлтые рёбра.</b> <b>R U R' U R U2 R' U</b> меняет местами переднее и левое
    ребро. Повторяй, пока все четыре не совпадут с центрами.</li>
<li><b>Расставь углы.</b> Держи угол, который уже на своём месте, спереди справа и
    делай <b>U R U' L' U R' U' L</b>, пока все углы не встанут.</li>
<li><b>Поверни углы.</b> Не поворачивая куб, повторяй <b>R' D' R D</b> для угла
    спереди справа, пока жёлтый не окажется сверху, затем крути только U, чтобы
    подвести следующий угол. В процессе куб выглядит разобранным — так и должно быть.</li>
</ol>
<p>Каждый алгоритм ниже отработай в тренажёре, пока не сделаешь его не глядя.</p>
""",
}

CFOP = {
    "en": """
<h2>From beginner to CFOP</h2>
<p>CFOP (the Fridrich method) is what most speedcubers use: <b>C</b>ross,
<b>F</b>2L, <b>O</b>LL, <b>P</b>LL. The fastest way to switch is to replace the last
layer first with the <b>2-look</b> sets: 10 algorithms for OLL and 6 for PLL.</p>
<p><b>2-look OLL:</b> first make the yellow cross (3 algorithms: line, L shape,
dot), then turn the corners (7 algorithms, recognised by the yellow stickers on the
sides).</p>
<p><b>2-look PLL:</b> first place the corners (T perm when two corners on one side
match — "headlights", Y perm otherwise), then the edges (Ua, Ub, H, Z).</p>
<p>When these feel easy, learn F2L, and later the full OLL and PLL.</p>
""",
    "ru": """
<h2>От метода новичка к CFOP</h2>
<p>CFOP (метод Фридрих) — метод большинства спидкуберов: <b>C</b>ross (крест),
<b>F</b>2L (два слоя), <b>O</b>LL (ориентация), <b>P</b>LL (расстановка).
Быстрее всего начать с последнего слоя и выучить наборы <b>в 2 этапа</b>:
10 алгоритмов для OLL и 6 для PLL.</p>
<p><b>OLL в 2 этапа:</b> сначала жёлтый крест (3 алгоритма: линия, уголок, точка),
потом углы (7 алгоритмов, их узнают по жёлтым наклейкам на боках).</p>
<p><b>PLL в 2 этапа:</b> сначала углы (T-перестановка, если на одной стороне два угла
совпадают — «фары», иначе Y-перестановка), потом рёбра (Ua, Ub, H, Z).</p>
<p>Когда это станет легко, учи F2L, а потом полный OLL и PLL.</p>
""",
}

F2L = {
    "en": """
<h2>F2L — first two layers</h2>
<p>Instead of corners and then edges, F2L pairs a white corner with its middle
edge on top and inserts both at once. Pictures show the front-right slot; grey
stickers belong to the last layer and don't matter.</p>
<ul>
<li>Start with the 4 basic inserts (F2L 1–4). Most other cases first bring the
    pieces into one of them.</li>
<li>Understand the moves rather than memorising them: watch what happens to the
    pair.</li>
<li>Use the same cases for the other slots by turning the cube with y.</li>
</ul>
""",
    "ru": """
<h2>F2L — первые два слоя</h2>
<p>Вместо «сначала углы, потом рёбра» в F2L белый угол соединяют с ребром второго
слоя наверху и вставляют их вместе. На картинках — слот спереди справа; серые
наклейки относятся к последнему слою и не важны.</p>
<ul>
<li>Начни с 4 базовых вставок (F2L 1–4). Почти все остальные случаи сначала сводятся к ним.</li>
<li>Старайся понять ходы, а не зазубрить: следи, что происходит с парой.</li>
<li>Для других слотов используй те же случаи, повернув куб (y).</li>
</ul>
""",
}

LESSONS = {"notation": NOTATION, "beginner": BEGINNER, "cfop": CFOP, "f2l": F2L}


def lesson_html(lesson_id, lang):
    data = LESSONS.get(lesson_id)
    if not data:
        return ""
    return data.get(lang) or data["en"]
