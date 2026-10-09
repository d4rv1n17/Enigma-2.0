# -*- coding: utf-8 -*-
"""Lessons for every event other than the 3x3 CFOP path (English / Russian)."""

L = {}

L["222-beginner"] = {
    "en": """<h2>2x2: beginner method</h2>
<p>A 2x2 is a 3x3 without edges and centres, so the beginner method needs only
4 algorithms. Pick a colour for the bottom (white).</p>
<ol>
<li><b>First layer.</b> Bring each white corner above its spot at front-right and repeat
<b>R U R' U'</b> until it drops in. Corners must also match each other on the sides.</li>
<li><b>Yellow on top.</b> Hold a corner whose yellow is not on top at front-left and do
<b>Sune: R U R' U R U2 R'</b>. Repeat (turning U between) until the whole top is yellow.</li>
<li><b>Place the top corners.</b> Look for two corners with the same colour on one side
("headlights"). Hold them at the back and do the <b>T perm</b>. If there are none, do the
<b>Y perm</b>. Finish with a U turn.</li>
</ol>""",
    "ru": """<h2>2x2: метод для начинающих</h2>
<p>2x2 — это 3x3 без рёбер и центров, поэтому методу новичка нужно всего 4 алгоритма.
Выбери цвет для низа (белый).</p>
<ol>
<li><b>Первый слой.</b> Поставь белый угол над его местом спереди справа и повторяй
<b>R U R' U'</b>, пока он не встанет. Углы должны совпадать и по бокам.</li>
<li><b>Жёлтый верх.</b> Держи угол, у которого жёлтый не сверху, спереди слева и делай
<b>Суне: R U R' U R U2 R'</b>. Повторяй (крутя U между повторами), пока весь верх не станет жёлтым.</li>
<li><b>Расставь верхние углы.</b> Найди два угла с одинаковым цветом на одной стороне
(«фары»). Держи их сзади и делай <b>T-перестановку</b>. Если «фар» нет — <b>Y-перестановку</b>.
В конце поверни U.</li>
</ol>""",
}

L["222-ortega"] = {
    "en": """<h2>Ortega method</h2>
<p>The most popular intermediate 2x2 method, usually 3 steps:</p>
<ol>
<li><b>One face</b> (any colour) on the bottom — the pieces don't need to match on the sides.</li>
<li><b>OLL:</b> make the opposite colour on top (7 algorithms).</li>
<li><b>PBL:</b> permute both layers at once (6 algorithms). Recognise the top and the bottom:
"Adj" = one adjacent swap, "Opp" = a diagonal swap.</li>
</ol>
<p>Next step: CLL — solve the first layer fully and the whole last layer in one algorithm.</p>""",
    "ru": """<h2>Метод Ортега</h2>
<p>Самый популярный метод для 2x2 после новичкового, обычно 3 шага:</p>
<ol>
<li><b>Одна грань</b> (любого цвета) снизу — по бокам детали можно не совмещать.</li>
<li><b>OLL:</b> противоположный цвет наверх (7 алгоритмов).</li>
<li><b>PBL:</b> расставить оба слоя сразу (6 алгоритмов). Смотри на верх и на низ:
«Adj» — обмен соседних углов, «Opp» — обмен по диагонали.</li>
</ol>
<p>Дальше — CLL: полностью собираешь первый слой, а весь последний — одним алгоритмом.</p>""",
}

L["444-reduction"] = {
    "en": """<h2>4x4: the reduction method</h2>
<p>Turn the 4x4 into a big 3x3, then solve it like a 3x3.</p>
<ol>
<li><b>Centres.</b> Build the 2x2 centres one by one: first two opposite colours, then the
remaining four. Use wide moves (<b>Rw</b>, <b>Uw</b>) and keep finished centres safe.</li>
<li><b>Edges.</b> Pair the two halves of each edge ("dedges"). Pair 8 edges with slice moves
and the last 4 using the "freeslice" trick.</li>
<li><b>3x3 stage.</b> Solve it like a 3x3, turning only outer layers.</li>
<li><b>Parity.</b> Two cases are impossible on a 3x3: a single flipped edge pair (OLL parity)
and two swapped edges (PLL parity). Each has its own algorithm below.</li>
</ol>
<p><b>5x5, 6x6, 7x7</b> are solved the same way: centres → edges → 3x3. A 5x5 has fixed centres,
so it never has PLL parity, only edge-pairing cases.</p>""",
    "ru": """<h2>4x4: метод редукции</h2>
<p>Превращаешь 4x4 в большой 3x3 и собираешь его как 3x3.</p>
<ol>
<li><b>Центры.</b> Собери центры 2x2 по очереди: сначала два противоположных цвета,
потом остальные четыре. Используй широкие ходы (<b>Rw</b>, <b>Uw</b>), не ломая готовые центры.</li>
<li><b>Рёбра.</b> Соедини половинки каждого ребра в пары. 8 рёбер — слайсами,
последние 4 — приёмом «freeslice».</li>
<li><b>Этап 3x3.</b> Собирай как 3x3, крутя только внешние слои.</li>
<li><b>Паритеты.</b> Два случая невозможны на 3x3: одна перевёрнутая пара рёбер
(OLL-паритет) и два переставленных ребра (PLL-паритет). Для каждого есть свой алгоритм.</li>
</ol>
<p><b>5x5, 6x6, 7x7</b> собираются так же: центры → рёбра → 3x3. У 5x5 центры
фиксированы, поэтому PLL-паритета нет — только случаи при сборке рёбер.</p>""",
}

L["555-edges"] = {
    "en": """<h2>5x5 and bigger cubes</h2>
<p>Use the same reduction as on the 4x4. Each edge has three pieces: first pair the middle
piece with one wing, then the other. When the last two edges are left, a single edge can
appear flipped — use the algorithm below.</p>
<p><b>6x6 and 7x7:</b> centres take most of the time. Solve them in the same order every time
and use 3Rw / 3Uw wide moves for the inner layers.</p>""",
    "ru": """<h2>5x5 и кубы больше</h2>
<p>Та же редукция, что и на 4x4. У каждого ребра три детали: сначала соедини середину
с одной половинкой, потом со второй. Когда остаются последние два ребра, одно может
оказаться перевёрнутым — для этого алгоритм ниже.</p>
<p><b>6x6 и 7x7:</b> больше всего времени занимают центры. Собирай их всегда в одном
порядке и используй широкие ходы 3Rw / 3Uw для внутренних слоёв.</p>""",
}

L["pyra-beginner"] = {
    "en": """<h2>Pyraminx: beginner method</h2>
<p><img src="move:pyram:" width="150"></p>
<ol>
<li><b>Tips.</b> Turn each of the 4 small tips (u, l, r, b) to match the centre piece under it.</li>
<li><b>Centres.</b> Turn the big layers so the three centres around each corner match.</li>
<li><b>First layer edges.</b> Solve the three edges around one face (the bottom). Use
<b>R U' R'</b> to insert an edge to the right and <b>L' U L</b> to the left.</li>
<li><b>Last edges.</b> Three cases remain: the edges cycle one way (Sune
<b>R U R' U R U R'</b>), the other way (<b>R U' R' U' R U' R'</b>) or two edges are flipped
(<b>R' L R L' U L' U' L</b>).</li>
</ol>
<p>Fast solvers use L4E or "top first" methods: see the L4E level.</p>""",
    "ru": """<h2>Пирамидка: метод для начинающих</h2>
<p><img src="move:pyram:" width="150"></p>
<ol>
<li><b>Вершинки.</b> Поверни каждую из 4 маленьких вершин (u, l, r, b) так, чтобы она совпала с центром под ней.</li>
<li><b>Центры.</b> Поверни большие слои, чтобы три центра вокруг каждой вершины совпали.</li>
<li><b>Рёбра первого слоя.</b> Собери три ребра вокруг одной грани (нижней).
<b>R U' R'</b> вставляет ребро вправо, <b>L' U L</b> — влево.</li>
<li><b>Последние рёбра.</b> Остаётся три случая: рёбра меняются по кругу в одну сторону
(Суне <b>R U R' U R U R'</b>), в другую (<b>R U' R' U' R U' R'</b>) или два ребра
перевёрнуты (<b>R' L R L' U L' U' L</b>).</li>
</ol>
<p>Быстрые сборщики используют L4E — смотри следующий уровень.</p>""",
}

L["pyra-l4e"] = {
    "en": """<h2>Pyraminx: L4E</h2>
<p>Solve the tips, the three centres and two edges around the bottom with intuition,
then finish the last four edges with one of 36 algorithms. If the result is off by one
turn of the top, finish with U or U'.</p>""",
    "ru": """<h2>Пирамидка: L4E</h2>
<p>Собери вершинки, три центра и два ребра вокруг низа интуитивно, а последние
четыре ребра — одним из 36 алгоритмов. Если в конце верх сдвинут на один поворот,
доверни U или U'.</p>""",
}

L["skewb-layer"] = {
    "en": """<h2>Skewb: layer method</h2>
<p>A Skewb has 8 corners and 6 centres; every move turns half of the puzzle around a corner.</p>
<ol>
<li><b>First layer</b> (by intuition): one centre and the 4 corners around it, all matching.
Hold it at the bottom.</li>
<li><b>Top corners.</b> After the first layer, the top corners are either solved or need one
of two cycles — two algorithms.</li>
<li><b>Last centres.</b> 3, 4 or 5 centres are left; match your case among the 16 pictures.</li>
</ol>
<p>The algorithms here were computed by Enigma Cube itself: each is the shortest possible
sequence in WCA notation and is checked by its tests.</p>""",
    "ru": """<h2>Скьюб: послойный метод</h2>
<p>У Скьюба 8 углов и 6 центров; каждый ход крутит половину головоломки вокруг угла.</p>
<ol>
<li><b>Первый слой</b> (интуитивно): один центр и 4 угла вокруг него, всё совпадает.
Держи его снизу.</li>
<li><b>Верхние углы.</b> После первого слоя верхние углы либо собраны, либо нужен один
из двух циклов — два алгоритма.</li>
<li><b>Последние центры.</b> Остаётся 3, 4 или 5 центров — найди свой случай среди 16 картинок.</li>
</ol>
<p>Алгоритмы вычислены самим Enigma Cube: каждый — кратчайший возможный в нотации WCA
и проверяется тестами.</p>""",
}

L["minx-beginner"] = {
    "en": """<h2>Megaminx: beginner method</h2>
<p>A megaminx is solved like a 3x3, just with more layers. Faces turn 72&deg; (one fifth).</p>
<ol>
<li><b>Star:</b> the 5 edges around the white face.</li>
<li><b>First layer corners</b> with R U R' U' like on a 3x3.</li>
<li><b>F2L, S2L, F3L…</b> layer by layer: insert edges and corner pairs, exactly as in the
3x3 beginner method.</li>
<li><b>Last layer in 4 looks:</b> edge orientation (EO), corner orientation (CO), edge
permutation (EP), corner permutation (CP).</li>
</ol>""",
    "ru": """<h2>Мегаминкс: метод для начинающих</h2>
<p>Мегаминкс собирается как 3x3, только слоёв больше. Грани поворачиваются на 72&deg; (пятую часть).</p>
<ol>
<li><b>Звезда:</b> 5 рёбер вокруг белой грани.</li>
<li><b>Углы первого слоя</b> через R U R' U', как на 3x3.</li>
<li><b>Второй, третий слой…</b> послойно: вставляешь рёбра и пары углов, как в методе новичка на 3x3.</li>
<li><b>Последний слой в 4 этапа:</b> ориентация рёбер (EO), ориентация углов (CO),
перестановка рёбер (EP), перестановка углов (CP).</li>
</ol>""",
}

L["sq1-beginner"] = {
    "en": """<h2>Square-1: beginner method</h2>
<p><img src="move:sq1:(1,0) /" width="200"></p>
<ol>
<li><b>Cube shape.</b> Move pieces between layers until both are squares (by intuition at
first). If the middle is not square, use the middle-layer algorithm.</li>
<li><b>Corners into layers</b>, then place the top corners.</li>
<li><b>Edges into layers</b> (swap edges between layers).</li>
<li><b>Bottom corners</b> and <b>edges</b> into place.</li>
<li><b>Parity:</b> if only two edges are swapped, use the parity algorithm.</li>
</ol>""",
    "ru": """<h2>Square-1: метод для начинающих</h2>
<p><img src="move:sq1:(1,0) /" width="200"></p>
<ol>
<li><b>Форма куба.</b> Перекладывай детали между слоями, пока оба не станут квадратами
(сначала интуитивно). Если средний слой не квадратный — алгоритм для среднего слоя.</li>
<li><b>Углы по слоям</b>, затем расставить верхние углы.</li>
<li><b>Рёбра по слоям</b> (обмен рёбер между слоями).</li>
<li><b>Нижние углы</b> и <b>рёбра</b> на места.</li>
<li><b>Паритет:</b> если поменяны только два ребра — алгоритм паритета.</li>
</ol>""",
}

L["clock-beginner"] = {
    "en": """<h2>Clock: beginner method</h2>
<p>The goal is to set all 18 clocks to 12. Pins up connect the clocks around them.</p>
<ol>
<li><b>Cross on the front:</b> use single pins (top-left, top-right, bottom-right) and then
both bottom pins to make the centre and the 4 edge clocks match, then all pins up and turn
everything to 12.</li>
<li><b>Same on the back:</b> turn the puzzle over (y2) and repeat.</li>
<li><b>Corners:</b> with one pin down at a time, match the centre and edges to that corner;
finish with all pins up.</li>
</ol>
<p>Never turn a dial whose pin is down — that moves clocks on the other side too.
Fast solvers use the 7-simul method (7 moves per side, both hands turning together).</p>""",
    "ru": """<h2>Clock: метод для начинающих</h2>
<p>Цель — выставить все 18 часов на 12. Поднятый штырёк соединяет часы вокруг себя.</p>
<ol>
<li><b>Крест спереди:</b> поднимая по одному штырьку (левый верхний, правый верхний,
правый нижний), а потом оба нижних, совмести центр и 4 «рёберных» часа; затем все штырьки
вверх — и всё на 12.</li>
<li><b>То же сзади:</b> переверни головоломку (y2) и повтори.</li>
<li><b>Углы:</b> опуская по одному штырьку, подгоняй центр и рёбра под этот угол;
в конце все штырьки вверх.</li>
</ol>
<p>Не крути колесо, чей штырёк опущен — сдвинутся часы и на другой стороне.
Быстрые сборщики используют метод 7-simul (7 ходов на сторону, обе руки одновременно).</p>""",
}

L["bld-op"] = {
    "en": """<h2>Blindfolded: Old Pochmann</h2>
<p>Memorise the cube, put on the blindfold, then solve one piece at a time.</p>
<ol>
<li><b>Lettering.</b> Give every sticker a letter (A–X) — edges and corners separately.</li>
<li><b>Memo.</b> Start at the buffer (edge UR, corner ULB) and follow where each piece
belongs, writing down the letters. Turn them into words or images.</li>
<li><b>Edges.</b> For each letter: set up the target to UL with moves that don't touch the
buffer, do the <b>T perm</b>, undo the setup. UB and UF have the Ja and Jb perms.</li>
<li><b>Parity.</b> If there is an odd number of edge targets, do one extra Ra perm.</li>
<li><b>Corners.</b> Same idea: set up the target to RDF and do the <b>modified Y perm</b>.</li>
</ol>""",
    "ru": """<h2>Вслепую: Old Pochmann</h2>
<p>Запоминаешь куб, надеваешь повязку и собираешь по одной детали.</p>
<ol>
<li><b>Буквы.</b> У каждой наклейки своя буква (A–X), отдельно для рёбер и углов.</li>
<li><b>Запоминание.</b> Начиная с буфера (ребро UR, угол ULB), идёшь по цепочке «куда
должна попасть деталь» и записываешь буквы. Превращаешь их в слова или образы.</li>
<li><b>Рёбра.</b> Для каждой буквы: подводишь цель на место UL ходами, не трогающими буфер,
делаешь <b>T-перестановку</b>, возвращаешь подводку. Для UB и UF — Ja и Jb.</li>
<li><b>Паритет.</b> Если целей у рёбер нечётное число — в конце одна Ra-перестановка.</li>
<li><b>Углы.</b> Так же: подводишь цель на RDF и делаешь <b>модифицированную Y</b>.</li>
</ol>""",
}

L["oh"] = {
    "en": """<h2>One-handed (OH)</h2>
<ul>
<li>Use the same CFOP method, but prefer algorithms with R, U and F moves only.</li>
<li>Turn U with the index finger, R by tilting the whole cube against the table or your palm.</li>
<li>Learn 2-look OLL/PLL first: the training path below applies to OH too.</li>
<li>A looser, well-lubricated cube helps a lot.</li>
</ul>""",
    "ru": """<h2>Одной рукой (OH)</h2>
<ul>
<li>Тот же CFOP, но выбирай алгоритмы только из ходов R, U и F.</li>
<li>U крути указательным пальцем, R — наклоняя весь куб о ладонь или стол.</li>
<li>Начни с OLL и PLL в 2 этапа — путь обучения 3x3 подходит и для OH.</li>
<li>Очень помогает более свободный, хорошо смазанный куб.</li>
</ul>""",
}

L["fmc"] = {
    "en": """<h2>Fewest moves (FMC)</h2>
<p>You have one hour and paper to find the shortest solution you can (WCA limit: 80 moves).</p>
<ul>
<li><b>Blocks:</b> build a 2x2x2, extend it to 2x2x3, then fix the edge orientation.</li>
<li><b>Look for skeletons:</b> solve all but 3–5 pieces, then use insertions of commutators.</li>
<li><b>NISS:</b> if you are stuck, continue on the inverse scramble.</li>
<li>Count every move (HTM: R2 = 1 move). A good beginner result is 40–50 moves.</li>
</ul>""",
    "ru": """<h2>Наименьшее число ходов (FMC)</h2>
<p>У тебя час и бумага, чтобы найти самое короткое решение (лимит WCA — 80 ходов).</p>
<ul>
<li><b>Блоки:</b> собери 2x2x2, расширь до 2x2x3, затем исправь ориентацию рёбер.</li>
<li><b>Ищи «скелеты»:</b> реши всё, кроме 3–5 деталей, и вставь коммутаторы.</li>
<li><b>NISS:</b> если застрял, продолжай на обратном скрамбле.</li>
<li>Считай каждый ход (HTM: R2 = 1 ход). Хороший результат для начала — 40–50 ходов.</li>
</ul>""",
}

L["roux"] = {
    "en": """<h2>Roux method</h2>
<p>Roux is the main alternative to CFOP, used by several world-class solvers. It needs few
algorithms and few moves (about 45), and relies on M-slice turns.</p>
<ol>
<li><b>First block:</b> a 1x2x3 block on the left (bottom-left edge, two side edges, two corners).</li>
<li><b>Second block:</b> the same 1x2x3 block on the right. Both blocks are built intuitively.</li>
<li><b>CMLL:</b> solve the four top corners in one algorithm without breaking the blocks
    (42 cases below; pictures show only the corners).</li>
<li><b>LSE (last six edges):</b> orient edges with M and U moves, place UL/UR, then solve the
    M slice. All intuitive.</li>
</ol>
<p>Tip: learn CMLL group by group (O, H, Pi, U, T, Sune, Anti Sune, L). If you know 2-look OLL,
start with the Sune, Anti Sune and Pi groups.</p>""",
    "ru": """<h2>Метод Roux</h2>
<p>Roux — главная альтернатива CFOP, им пользуются несколько сборщиков мирового уровня. В нём мало
алгоритмов и ходов (около 45), зато много поворотов среднего слоя M.</p>
<ol>
<li><b>Первый блок:</b> блок 1x2x3 слева (нижнее левое ребро, два боковых ребра, два угла).</li>
<li><b>Второй блок:</b> такой же блок 1x2x3 справа. Оба блока собираются интуитивно.</li>
<li><b>CMLL:</b> четыре верхних угла одним алгоритмом, не ломая блоки
    (42 случая ниже; на картинках цветные только углы).</li>
<li><b>LSE (последние шесть рёбер):</b> ориентация рёбер ходами M и U, установка UL/UR, затем
    средний слой. Всё интуитивно.</li>
</ol>
<p>Совет: учи CMLL по группам (O, H, Pi, U, T, Sune, Anti Sune, L). Если знаешь OLL в 2 этапа,
начни с групп Sune, Anti Sune и Pi.</p>""",
}

L["cross"] = {
    "en": """<h2>The cross: plan it during inspection</h2>
<p>Fast solvers plan the whole cross in the 15 seconds of inspection and do it on the
<b>bottom</b>, so they can already look for the first F2L pair.</p>
<ol>
<li><b>Find the four white edges</b> and their side colours before you touch the cube.</li>
<li><b>Solve edges relative to each other,</b> not to the centres: two edges that are opposite
    (white-green and white-blue) or next to each other must keep that relation. One final
    D move then lines all of them up.</li>
<li><b>Aim for 8 moves or fewer.</b> Every cross can be solved in at most 8 moves.</li>
<li><b>Do it upside down:</b> practise building the cross on the bottom from the start.</li>
</ol>
<h3>Drills</h3>
<ul>
<li>Scramble, inspect for 15 seconds, then solve the cross <b>blindfolded</b> (eyes closed).</li>
<li>Count your moves; try again with a shorter plan.</li>
<li>Later: learn to use any colour (colour neutrality) — it gives easier crosses.</li>
</ul>""",
    "ru": """<h2>Крест: планируй на инспекции</h2>
<p>Быстрые сборщики продумывают весь крест за 15 секунд инспекции и собирают его
<b>снизу</b>, чтобы сразу искать первую пару F2L.</p>
<ol>
<li><b>Найди все четыре белых ребра</b> и их боковые цвета, ещё не трогая куб.</li>
<li><b>Ставь рёбра относительно друг друга,</b> а не центров: противоположные рёбра
    (бело-зелёное и бело-синее) или соседние должны сохранять это положение. В конце
    один ход D выровняет все сразу.</li>
<li><b>Цель — не больше 8 ходов.</b> Любой крест решается максимум за 8 ходов.</li>
<li><b>Собирай снизу:</b> с самого начала тренируй крест на нижней грани.</li>
</ol>
<h3>Упражнения</h3>
<ul>
<li>Скрамбл, 15 секунд инспекции, затем крест <b>с закрытыми глазами</b>.</li>
<li>Считай ходы и попробуй найти план короче.</li>
<li>Позже: научись начинать с любого цвета (цветовая нейтральность) — кресты станут проще.</li>
</ul>""",
}

L["fingertricks"] = {
    "en": """<h2>Finger tricks</h2>
<p>Speed comes from turning with your fingers instead of re-gripping the cube.</p>
<ul>
<li><b>Home grip:</b> thumbs on the front, index fingers on top, the rest of the fingers
    behind. Hold the cube loosely.</li>
<li><b>U:</b> push the back-right of the top layer with your right index finger.
    <b>U'</b>: the same with the left index finger.</li>
<li><b>R / R':</b> turn with the right wrist, not the whole arm. Keep the thumb on the front.</li>
<li><b>F:</b> right thumb pushes up the front, or index finger pulls from the top.</li>
<li><b>D:</b> left ring finger pulls the bottom layer towards you.</li>
<li><b>M':</b> push the middle slice up with the left ring finger (used in Roux and OLL).</li>
</ul>
<h3>How to practise</h3>
<ul>
<li>Take an algorithm you know (Sune: R U R' U R U2 R') and repeat it 20 times without
    looking, slowly and without pauses. Then a bit faster.</li>
<li>Smooth turning without pauses beats fast turning with pauses.</li>
</ul>""",
    "ru": """<h2>Фингертрики</h2>
<p>Скорость появляется, когда крутишь пальцами, а не перехватываешь куб.</p>
<ul>
<li><b>Базовый хват:</b> большие пальцы спереди, указательные сверху, остальные сзади.
    Держи куб свободно.</li>
<li><b>U:</b> толкни верхний слой сзади справа правым указательным пальцем.
    <b>U'</b>: то же левым указательным.</li>
<li><b>R / R':</b> поворот кистью, а не всей рукой. Большой палец остаётся спереди.</li>
<li><b>F:</b> правый большой палец толкает переднюю грань вверх, или указательный тянет сверху.</li>
<li><b>D:</b> левый безымянный палец тянет нижний слой к себе.</li>
<li><b>M':</b> левый безымянный толкает средний слой вверх (нужно в Roux и OLL).</li>
</ul>
<h3>Как тренировать</h3>
<ul>
<li>Возьми знакомый алгоритм (Суне: R U R' U R U2 R') и повтори его 20 раз не глядя —
    медленно и без пауз. Потом чуть быстрее.</li>
<li>Плавная сборка без пауз быстрее, чем резкая с остановками.</li>
</ul>""",
}

L["lookahead"] = {
    "en": """<h2>Look-ahead and a practice plan</h2>
<p><b>Look-ahead</b> means finding the next F2L pair while you are still inserting the
current one. It is the biggest difference between 30 and 15 seconds.</p>
<ol>
<li><b>Slow solves:</b> solve so slowly that you never stop. If you stop to look, go slower.</li>
<li><b>Watch the pieces, not your hands.</b> During an insertion your eyes should already
    move to the rest of the cube.</li>
<li><b>Fewer cube rotations:</b> learn F2L cases from the back slots too, so you can keep
    tracking pieces.</li>
</ol>
<h3>A simple weekly plan</h3>
<ul>
<li>Every day: 10 minutes of algorithm review in the trainer (it shows what is due).</li>
<li>Every day: one session of 50 solves in the timer — watch your ao12, not single times.</li>
<li>Twice a week: 10 slow look-ahead solves and 10 blindfolded crosses.</li>
<li>Learn 3–4 new cases a day at most — the trainer introduces them for you.</li>
</ul>
<p>Typical milestones: sub-60 with the beginner method, sub-30 with 2-look OLL/PLL and F2L,
sub-20 with full OLL/PLL and good look-ahead.</p>""",
    "ru": """<h2>Look-ahead и план тренировок</h2>
<p><b>Look-ahead</b> — умение искать следующую пару F2L, пока вставляешь текущую. Это главное,
что отличает 30 секунд от 15.</p>
<ol>
<li><b>Медленные сборки:</b> собирай так медленно, чтобы ни разу не остановиться. Если
    остановился посмотреть — собирай ещё медленнее.</li>
<li><b>Следи за деталями, а не за руками.</b> Пока вставляешь пару, глаза уже ищут следующую.</li>
<li><b>Меньше поворотов куба:</b> выучи случаи F2L и для задних слотов, чтобы не терять детали
    из виду.</li>
</ol>
<h3>Простой план на неделю</h3>
<ul>
<li>Каждый день: 10 минут повторения в тренажёре (он сам покажет, что пора повторить).</li>
<li>Каждый день: сессия из 50 сборок в таймере — смотри на ao12, а не на синглы.</li>
<li>Два раза в неделю: 10 медленных сборок на look-ahead и 10 крестов вслепую.</li>
<li>Не больше 3–4 новых случаев в день — тренажёр сам вводит их постепенно.</li>
</ul>
<p>Обычные ориентиры: быстрее 60 секунд — метод для начинающих, быстрее 30 — OLL и PLL в 2 этапа
плюс F2L, быстрее 20 — полный OLL/PLL и хороший look-ahead.</p>""",
}
