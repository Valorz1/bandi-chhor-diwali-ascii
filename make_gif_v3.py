import math, os, random
import pyfiglet
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops


def find_font(font_name, bold=False):
    candidates = []
    base_names = [font_name, font_name.replace("SansMono", "Mono"), font_name.replace("SansMono", "Mono"), font_name.replace("Mono", "SansMono")]
    if bold:
        base_names = [name.replace(".ttf", "-Bold.ttf") if ".ttf" in name else name for name in base_names]
    for base in base_names:
        candidates.extend([
            base,
            os.path.join("/usr/share/fonts/truetype/dejavu", base),
            os.path.join("/usr/share/fonts/truetype/liberation2", base),
            os.path.join("C:\\Windows\\Fonts", base),
            os.path.join("C:\\Windows\\Fonts", base.lower()),
        ])
    candidates.extend([
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
        "C:\\Windows\\Fonts\\CascadiaMono.ttf",
        "C:\\Windows\\Fonts\\CascadiaCode.ttf",
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\consolab.ttf",
    ])
    seen = set()
    for path in candidates:
        if not path or path in seen:
            continue
        seen.add(path)
        if os.path.exists(path):
            return ImageFont.truetype(path, FS)
    return ImageFont.load_default()


random.seed(21)
FS = 12
FONT = find_font("DejaVuSansMono.ttf")
FONTB = find_font("DejaVuSansMono-Bold.ttf", bold=True)
CW = 7.25
CH = 14
PAD = 12
N = 60
W = 132

GOLD = (255, 196, 60)
GOLD2 = (255, 170, 40)
DGOLD = (190, 125, 30)
WATER = (30, 70, 150)
MIR = {"/": "\\", "\\": "/", "(": ")", ")": "(", "[": "]", "]": "[", "<": ">", ">": "<"}


def mirror_full(half):
    return half + "".join(MIR.get(c, c) for c in reversed(half[:-1]))


def check_sym(s):
    assert s == "".join(MIR.get(c, c) for c in reversed(s)), s


# ======================= TEMPLE =======================
HALF = 36  # left half incl. centre col (index 35)
C = HALF - 1

DOME = [
    ".",
    "|",
    "/^\\",
    "(_o_)",
    ".-'''-.",
    ".'(  |  )'.",
    ".'( (  |  ) )'.",
    "/( ( (  |  ) ) )\\",
    "|( ( ( (  |  ) ) ) )|",
    "|( ( ( (  |  ) ) ) )|",
    "\\( ( ( (  |  ) ) ) )/",
    "'-._______________.-'",
    "[" + "o:" * 10 + "o]",
    "|" + "=" * 21 + "|",
]
for d in DOME:
    check_sym(d)

BIG_CH = ["   .   ", "  /^\\  ", " (___) ", " |:|:| ", " |_|_| "]
SMALL_CH = ["  .  ", " /^\\ ", "(___)", " |:| "]


def body_row(kind):
    s = []
    for i in range(HALF):
        if i == 0:
            s.append({"top": " ", "eave": "=", "floor": "|", "plinth": "["}.get(kind, "|"))
            continue
        d6 = (C - i) % 6
        d8 = (C - i) % 8
        ch = " "
        if kind == "top":
            ch = "_"
        elif kind == "jali":
            ch = "x" if i % 2 == 1 else ":"
        elif kind == "eave":
            ch = "="
        elif kind == "corbel":
            ch = "v" if i % 2 == 1 else "_"
        elif kind == "u_top":
            ch = "-" if d6 == 0 else "." if d6 in (1, 5) else "_" if d6 == 3 else " "
        elif kind == "u_mid":
            ch = "|" if d6 in (1, 5) else ":" if d6 == 3 else " "
        elif kind == "u_floor":
            ch = "|" if d6 in (1, 5) else "_"
        elif kind == "band":
            ch = "o" if i % 2 == 1 else "-"
        elif kind == "l_top":
            ch = "-" if d8 in (0, 1, 7) else "." if d8 in (2, 6) else " "
        elif kind == "l_mid":
            ch = "|" if d8 in (2, 6) else "*" if d8 == 4 else " "
        elif kind == "l_mid2":
            ch = "|" if d8 in (2, 6) else ":" if d8 == 4 else " "
        elif kind == "floor":
            ch = "|" if d8 in (2, 6) else "_"
        elif kind == "plinth":
            ch = "=" if i % 4 else "#"
        s.append(ch)
    return "".join(s)


halves = []
for r, d in enumerate(DOME):
    dh = d[: len(d) // 2 + 1]
    side = [" "] * (HALF - len(dh))
    k = r - (len(DOME) - 5)
    if k >= 0:
        for j, ch in enumerate(BIG_CH[k]):
            side[1 + j] = ch
    k2 = r - (len(DOME) - 4)
    if k2 >= 0:
        for j, ch in enumerate(SMALL_CH[k2]):
            side[11 + j] = ch
    halves.append("".join(side) + dh)
for kind in ["top", "jali", "eave", "u_top", "u_mid", "u_mid", "u_floor", "band", "corbel",
             "l_top", "l_mid2", "l_mid", "l_mid2", "floor", "plinth"]:
    halves.append(body_row(kind))
TEMPLE = [mirror_full(h) for h in halves]
TW = len(TEMPLE[0])
LIT = set()  # (r, c) cells inside arches -> glow
for r, line in enumerate(TEMPLE):
    if r >= len(DOME) + 4:
        inside = False
        for c, ch in enumerate(line):
            if ch == "|":
                inside = not inside
            elif inside and ch == " ":
                LIT.add((r, c))

GATE = [
    "     .     ",
    "   _/^\\_   ",
    "  (_____)  ",
    " _|_____|_ ",
    "|:x:x:x:x:|",
    "|  .---.  |",
    "|::|   |::|",
    "|::|   |::|",
    "|__|___|__|",
]
for g in GATE:
    check_sym(g)

# ======================= LAYOUT =======================
TY = 21
TX = W - TW - 6
BASE_Y = TY + len(TEMPLE)
WATER_ROWS = 12
GX, GY = 6, BASE_Y - len(GATE)
DIYA_Y = BASE_Y + WATER_ROWS + 2
H = DIYA_Y + 6

B1 = [l for l in pyfiglet.figlet_format("Bandi Chhor Divas", font="small", width=300).split("\n") if l.strip()]
B2 = [l for l in pyfiglet.figlet_format("Happy Diwali", font="small", width=300).split("\n") if l.strip()]
SUB = "~ celebrating light, freedom & the return of Guru Hargobind Sahib Ji to Amritsar ~"
SUB_Y = 12

stars = [(random.randrange(W), random.randrange(0, BASE_Y - 6), random.random() * 6.28,
          random.choice([1, 2, 3])) for _ in range(150)]

lanterns = [dict(x=random.uniform(4, W - 4), off=random.random(), sway=random.random() * 6.28,
                 speed=random.choice([1, 1, 2])) for _ in range(9)]

FW_COLORS = [(255, 70, 90), (70, 210, 255), (255, 110, 240), (110, 255, 130),
             (255, 215, 90), (255, 150, 50), (170, 130, 255), (255, 255, 255)]


def make_burst(start, x):
    kind = random.choice(["peony", "peony", "willow", "ring", "crossette"])
    col = random.choice(FW_COLORS)
    col2 = random.choice(FW_COLORS)
    parts = []
    n = 40 if kind != "ring" else 30
    big = random.uniform(0.9, 1.25)
    for i in range(n):
        a = 2 * math.pi * i / n + random.uniform(-0.06, 0.06)
        sp = 1.0 if kind == "ring" else random.uniform(0.35, 1.0)
        if kind == "ring" and i % 2:
            sp = 0.55
        parts.append((math.cos(a) * sp * 2.1 * big, math.sin(a) * sp * big, col if i % 3 else col2))
    return dict(kind=kind, x=x, y=random.randrange(16, 25), start=start, rise=7,
                life=20 if kind == "willow" else 16, parts=parts)


xs = [14, 100, 40, 118, 66, 26, 88, 54, 110, 76, 34, 122]
bursts = [make_burst((i * N // len(xs)) % N, xs[i] + random.randrange(-3, 4)) for i in range(len(xs))]

DIYA_XS = list(range(5, W - 3, 9))
FLAME_TIP = ["'", ".", "'", "`", "'", ","]
FLAME_BODY = ["(", "^", ")", "^", "A", "^"]


def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def burst_particles(b, f):
    """yield (x, y, ch, col, bold) for a burst at frame f"""
    t = (f - b["start"]) % N
    out = []
    if t < b["rise"]:
        y = BASE_Y - 1 - (BASE_Y - 1 - b["y"]) * (t + 1) / b["rise"]
        wob = math.sin(t * 1.7) * 0.4
        out.append((b["x"] + wob, y, "|", (255, 235, 170), True))
        out.append((b["x"], y + 1, ":", (220, 160, 80), False))
        out.append((b["x"], y + 2, ".", (140, 100, 60), False))
        return out
    if t >= b["rise"] + b["life"]:
        return out
    age = t - b["rise"]
    p = age / b["life"]
    g = 0.03 if b["kind"] != "willow" else 0.045
    for k, (vx, vy, col) in enumerate(b["parts"]):
        drag = (1 - 0.9 ** (age + 1)) / 0.1
        x = b["x"] + vx * drag
        y = b["y"] + vy * drag + g * age * age
        if b["kind"] == "willow":
            c = lerp((255, 230, 140), (130, 70, 20), p)
        elif p < 0.35:
            c = lerp((255, 255, 255), col, p / 0.35)
        else:
            c = lerp(col, (25, 15, 45), (p - 0.35) / 0.65)
        ch = "@" if p < 0.1 else "*" if p < 0.45 else "+" if p < 0.7 else "."
        if b["kind"] == "crossette" and p > 0.45:
            # split into little crosses
            for dx, dy in ((1, 0), (-1, 0), (0, 0)):
                out.append((x + dx * (p - 0.4) * 4, y + dy, "+" if dx == 0 else "-", c, False))
            continue
        # crackle / twinkle late in life
        if p > 0.6 and (k + f) % 3 == 0:
            continue
        out.append((x, y, ch, c, p < 0.5))
        if p > 0.08:
            for back in (1, 2):
                if age - back < 0:
                    continue
                d2 = (1 - 0.9 ** (age + 1 - back)) / 0.1
                x2 = b["x"] + vx * d2
                y2 = b["y"] + vy * d2 + g * (age - back) ** 2
                tc = lerp(c, (20, 15, 40), 0.35 * back)
                out.append((x2, y2, "'" if b["kind"] == "willow" else ".", tc, False))
    if age < 2:
        out.append((b["x"], b["y"], "#", (255, 255, 255), True))
    return out


def render(f):
    grid = {}
    TT = 2 * math.pi * f / N  # loop phase

    def put(x, y, ch, col, bold=False):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < W and 0 <= y < H and ch != " ":
            grid[(x, y)] = (ch, col, bold)

    def clear_rect(x0, y0, x1, y1):
        for (x, y) in list(grid):
            if x0 <= x <= x1 and y0 <= y <= y1:
                del grid[(x, y)]

    def mask_block(lines, x0, y0):
        for r, line in enumerate(lines):
            s = len(line) - len(line.lstrip())
            e = len(line.rstrip())
            for c in range(s, e):
                grid.pop((x0 + c, y0 + r), None)

    # ---- stars ----
    for sx, sy, ph, sp in stars:
        v = math.sin(TT * sp + ph)
        if v > 0.8:
            put(sx, sy, "*", (240, 240, 255))
        elif v > 0.3:
            put(sx, sy, "+", (170, 170, 220))
        elif v > -0.3:
            put(sx, sy, ".", (120, 120, 180))

    # ---- sky lanterns (rising, swaying) ----
    for L in lanterns:
        prog = (f / N * L["speed"] + L["off"]) % 1.0
        y = BASE_Y - 3 - prog * (BASE_Y - 4)
        x = L["x"] + math.sin(TT * 2 + L["sway"]) * 1.2
        fade = min(1, (1 - prog) * 2.5)
        body = lerp((40, 20, 30), (255, 150, 50), fade)
        put(x - 1, y, "[", body, True)
        put(x, y, "#" if f % 2 else "=", lerp((40, 20, 30), (255, 220, 120), fade), True)
        put(x + 1, y, "]", body, True)
        put(x, y + 1, "'", lerp((40, 20, 30), (255, 200, 90), fade))

    # ---- fireworks ----
    reflections = []
    for b in bursts:
        for (x, y, ch, col, bold) in burst_particles(b, f):
            if y < BASE_Y - 1:
                put(x, y, ch, col, bold)
                ry = BASE_Y + 1 + (BASE_Y - y) * 0.28
                if BASE_Y < ry < BASE_Y + WATER_ROWS and ch in "@*+#":
                    reflections.append((x + math.sin(ry + TT * 3) * 0.6, ry, lerp(col, WATER, 0.45)))

    # ---- banner ----
    clear_rect(0, 0, W, SUB_Y)

    def banner(lines, y0, off):
        w = max(len(l) for l in lines)
        x0 = (W - w) // 2
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                k = 0.5 + 0.5 * math.sin(c * 0.16 - TT * 3 + off)
                put(x0 + c, y0 + r, ch, lerp((255, 110, 20), (255, 240, 140), k), True)

    banner(B1, 1, 0)
    banner(B2, 6, 1.7)
    n = min(len(SUB), int(f * 2.2))
    sx = (W - len(SUB)) // 2
    for i, ch in enumerate(SUB[:n]):
        put(sx + i, SUB_Y, ch, (235, 205, 165))
    if n < len(SUB) and f % 2 == 0:
        put(sx + n, SUB_Y, "_", (255, 255, 255))
    # little diya ornaments either side of subtitle
    for ox in (sx - 4, sx + len(SUB) + 3):
        put(ox, SUB_Y - 1, FLAME_BODY[f % 6], (255, 170, 50), True)
        put(ox - 1, SUB_Y, "\\", (220, 110, 50), True)
        put(ox, SUB_Y, "_", (220, 110, 50), True)
        put(ox + 1, SUB_Y, "/", (220, 110, 50), True)

    # ---- Nishan Sahib (waving) ----
    fx, fy = GX + len(GATE[0]) + 6, BASE_Y - 22
    mask_block([" " * 14] * 8, fx, fy)
    for y in range(fy, BASE_Y - 1):
        put(fx, y, "|", (215, 215, 225), True)
    put(fx, fy - 1, "^", (235, 235, 240), True)
    put(fx, fy - 2, ".", (255, 255, 255), True)
    for r in range(7):
        length = 12 - abs(r - 3) * 3
        for c in range(1, length + 1):
            sh = math.sin(TT * 5 - c * 0.55) * 0.9 * (c / 12)
            ch = ">" if c == length else "#"
            k = 0.5 + 0.5 * math.sin(TT * 5 - c * 0.55 - r * 0.3)
            put(fx + c, fy + r + sh, ch, lerp((215, 95, 5), (255, 195, 75), k), True)

    # ---- Darshani Deori gateway ----
    mask_block(GATE, GX, GY)
    for r, line in enumerate(GATE):
        for c, ch in enumerate(line):
            col = GOLD
            if r >= 6 and 4 <= c <= 6:
                col = (255, 140, 30)
                ch = ":" if (r + f // 4) % 2 else " "
            put(GX + c, GY + r, ch, col, True)
    put(GX + 5, GY - 1, "*" if (f // 3) % 2 else "+", (255, 245, 180), True)

    # ---- causeway (Guru's bridge) with lamp posts ----
    cw0, cw1 = GX + len(GATE[0]), TX
    for x in range(0, TX + TW + 3):
        put(x, BASE_Y, "=", DGOLD, True)
    for x in range(cw0, cw1):
        put(x, BASE_Y - 1, "|" if x % 3 == 0 else "_", DGOLD)
    for i, lx in enumerate(range(cw0 + 3, cw1 - 1, 7)):
        put(lx, BASE_Y - 2, "|", (170, 150, 120))
        put(lx, BASE_Y - 3, "|", (170, 150, 120))
        lc = [(255, 245, 190), (255, 200, 90), (255, 170, 60)][(f + i) % 3]
        put(lx, BASE_Y - 4, "o", lc, True)
        put(lx - 1, BASE_Y - 4, "(", (200, 160, 80))
        put(lx + 1, BASE_Y - 4, ")", (200, 160, 80))
        # lamp reflection streak
        for k in range(1, 5):
            if (k + f + i) % 3:
                put(lx + math.sin(TT * 4 + k) * 0.7, BASE_Y + k, "|" if k < 3 else ":", lerp(lc, WATER, 0.25 + k * 0.15))

    # ---- temple ----
    mask_block(TEMPLE, TX, TY)
    for r, line in enumerate(TEMPLE):
        for c, ch in enumerate(line):
            col = GOLD
            if r < len(DOME) and ch in "()" and 4 < r < len(DOME) - 3:
                col = GOLD2
            if ch == "o":
                col = (255, 250, 200) if (c + f) % 4 < 2 else (255, 160, 50)
            if ch in "x:" and r == len(DOME) + 1:
                col = (255, 215, 110)
            put(TX + c, TY + r, ch, col, True)
            if (r, c) in LIT:
                v = math.sin(TT * 3 + c * 0.7 + r)
                put(TX + c, TY + r, "*" if v > 0.7 else ":" if v > -0.2 else ".", lerp((200, 90, 20), (255, 200, 90), 0.5 + 0.5 * v), True)
    # rooftop lamps
    tops = [(TX + C, TY - 1)]
    for r, line in enumerate(TEMPLE[: len(DOME)]):
        for c, ch in enumerate(line):
            if ch == "." and c != C and r < len(DOME) - 3:
                tops.append((TX + c, TY + r - 1))
    for i, (lx, ly) in enumerate(tops):
        put(lx, ly, "*" if (f // 2 + i) % 2 else "+", (255, 248, 190), True)

    # ---- sarovar ----
    for wr in range(WATER_ROWS):
        y = BASE_Y + 1 + wr
        depth = wr / WATER_ROWS
        src = len(TEMPLE) - 1 - int(wr * 2.4)
        gsrc = len(GATE) - 1 - int(wr * 1.4)
        for x in range(W):
            if (x, y) in grid:
                continue
            shift = int(round(math.sin(TT * 4 + wr * 0.9 + x * 0.12) * (0.5 + depth * 1.3)))
            ch, col = " ", WATER
            if 0 <= src < len(TEMPLE):
                c = x - TX + shift
                if 0 <= c < TW and TEMPLE[src][c] != " ":
                    ch = TEMPLE[src][c]
                    col = lerp(GOLD, WATER, 0.3 + depth * 0.55)
            if ch == " " and 0 <= gsrc < len(GATE):
                c = x - GX + shift
                if 0 <= c < len(GATE[0]) and GATE[gsrc][c] != " ":
                    ch = GATE[gsrc][c]
                    col = lerp(GOLD, WATER, 0.35 + depth * 0.55)
            if ch == " " and wr == 0 and x < TX:
                ch, col = "-", lerp(DGOLD, WATER, 0.55)
            if ch == " ":
                if (x * 7 + wr * 13 + f) % 15 == 0:
                    ch = "~"
                elif (x * 3 + wr * 5 - f) % 19 == 0:
                    ch = "-"
                elif (x * 11 + wr * 3 + 2 * f) % 41 == 0:
                    ch = "."
                col = lerp((80, 130, 220), WATER, depth)
            put(x, y, ch, col)
    for (x, y, col) in reflections:
        key = (int(round(x)), int(round(y)))
        if key not in grid or grid[key][0] in "~-.":
            put(x, y, "*" if y < BASE_Y + 4 else ".", col)

    # ---- ghat with diyas ----
    for x in range(W):
        put(x, DIYA_Y + 2, "=" if x % 2 else "-", (130, 75, 40))
    for i, dx in enumerate(DIYA_XS):
        ph = (f + i * 2) % 6
        tipc = (255, 240, 170)
        bodyc = [(255, 225, 90), (255, 160, 40), (255, 120, 30)][(f + i) % 3]
        if (f + i) % 3 != 1:
            put(dx, DIYA_Y - 2, FLAME_TIP[ph], tipc)
        put(dx, DIYA_Y - 1, FLAME_BODY[ph], bodyc, True)
        put(dx, DIYA_Y, "|", (255, 200, 120), True)
        put(dx - 2, DIYA_Y, ".", (220, 110, 50), True)
        put(dx + 2, DIYA_Y, ".", (220, 110, 50), True)
        put(dx - 3, DIYA_Y + 1, "\\", (220, 110, 50), True)
        for k in (-2, -1, 1, 2):
            put(dx + k, DIYA_Y + 1, "_", (220, 110, 50), True)
        put(dx, DIYA_Y + 1, "o", (255, 190, 70), True)
        put(dx + 3, DIYA_Y + 1, "/", (220, 110, 50), True)
        # rangoli dots between diyas
        mx = dx + 4
        rc = [(255, 80, 130), (80, 230, 170), (120, 160, 255), (255, 200, 60)][(i + f // 4) % 4]
        put(mx, DIYA_Y, "*", rc, True)
        put(mx - 1, DIYA_Y + 1, "<", rc)
        put(mx + 1, DIYA_Y + 1, ">", rc)
        put(mx, DIYA_Y + 1, "o", rc, True)

    # ---- rangoli border (2 rows) ----
    cols = [(255, 80, 130), (255, 200, 60), (80, 230, 170), (120, 160, 255), (255, 130, 50)]
    for row, pat, sgn in ((DIYA_Y + 3, "<*>-o-", 1), (DIYA_Y + 4, "-o-<*>", -1)):
        off = (f * sgn) % len(pat)
        for x in range(W):
            put(x, row, pat[(x + off) % len(pat)], cols[(x // 6 + f // 3 + row) % len(cols)], True)

    # ---- draw ----
    iw, ih = int(W * CW) + 2 * PAD, H * CH + 2 * PAD
    img = Image.new("RGB", (iw, ih))
    d = ImageDraw.Draw(img)
    horizon = PAD + BASE_Y * CH
    for yy in range(ih):
        if yy < horizon:
            col = lerp((5, 5, 20), (48, 20, 64), (yy / horizon) ** 1.4)
        else:
            col = lerp((14, 22, 55), (4, 8, 22), (yy - horizon) / (ih - horizon))
        d.line([(0, yy), (iw, yy)], fill=col)
    txt = Image.new("RGB", img.size, (0, 0, 0))
    dt = ImageDraw.Draw(txt)
    for (x, y), (ch, col, bold) in grid.items():
        dt.text((PAD + x * CW, PAD + y * CH), ch, fill=col, font=FONTB if bold else FONT)
    bloom = txt.filter(ImageFilter.GaussianBlur(6)).point(lambda v: min(255, int(v * 1.7)))
    img = ImageChops.screen(img, bloom)
    img = ImageChops.screen(img, txt)
    return img


if __name__ == "__main__":
    import sys
    frames = [render(f) for f in range(N)]
    pal = Image.new("RGB", (frames[0].width, frames[0].height * 3))
    for i, k in enumerate((10, 30, 50)):
        pal.paste(frames[k], (0, frames[0].height * i))
    pal = pal.quantize(colors=200, method=Image.Quantize.MEDIANCUT)
    q = [fr.quantize(palette=pal, dither=Image.Dither.NONE) for fr in frames]
    q[0].save("bandi_chhor_diwali_hd.gif", save_all=True, append_images=q[1:], duration=85, loop=0, optimize=True)
    for k in (12, 33):
        frames[k].save(f"hd{k}.png")
    print("done", frames[0].size)
