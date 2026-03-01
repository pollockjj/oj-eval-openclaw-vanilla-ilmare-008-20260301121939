#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
CODE.mkdir(exist_ok=True)


def write(name: str, lines: list[str]) -> None:
    (CODE / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def gen_2276() -> None:
    s = "Hello World!"
    lines = [f"O<{ord(c)}" for c in s]
    lines.append("Z<1")
    write("2276.mv", lines)


def gen_2277() -> None:
    lines = [
        "[1000]<48",
        "[1001]<49",
        "A<I",
        "[A]<1",
        "B<I",
        "C<[B]",
        "O<[C+1000]",
        "Z<1",
    ]
    write("2277.mv", lines)


def gen_2278() -> None:
    lines: list[str] = []
    base = 2048
    for i in range(10):
        lines.append(f"[{base + 48 + i}]<{48 + ((i + 1) % 10)}")
    lines += [
        "A<I",
        f"B<[A+{base}]",
        "O<B",
        "Z<1",
    ]
    write("2278.mv", lines)


def gen_2279() -> None:
    lines = [
        "[3000]<1",
        "A<I",
        "Z<[A+3000]",
        "O<A",
    ]
    write("2279.mv", lines)


def gen_2280() -> None:
    hb = 0
    tb = 256
    ub = 512
    lines: list[str] = []
    for x in range(256):
        s = str(x)
        h = ord(s[0]) if len(s) == 3 else 0
        t = ord(s[-2]) if len(s) >= 2 else 0
        u = ord(s[-1])
        lines.append(f"[{hb + x}]<{h}")
        lines.append(f"[{tb + x}]<{t}")
        lines.append(f"[{ub + x}]<{u}")
    lines += [
        "A<I",
        f"O<[A+{hb}]",
        f"O<[A+{tb}]",
        f"O<[A+{ub}]",
        "Z<1",
    ]
    write("2280.mv", lines)


def gen_2281() -> None:
    ID_BASE = 0
    ROW10_BASE = 100
    ADD2_BASE = 110
    ROW2_BASE = 210
    ONES_BASE = 229
    CARRY_BASE = 267
    DIGIT_BASE = 400
    ASCII_BASE = 460
    ASCII_FIRST_BASE = 470

    ARR1 = 480
    ARR2 = 490
    OUT = 500
    CARRY = 511

    lines: list[str] = []

    for i in range(100):
        lines.append(f"[{ID_BASE + i}]<{i}")

    for d in range(10):
        lines.append(f"[{ROW10_BASE + d}]<{d * 10}")

    for a in range(10):
        for b in range(10):
            idx = a * 10 + b
            lines.append(f"[{ADD2_BASE + idx}]<{a + b}")

    for s in range(19):
        lines.append(f"[{ROW2_BASE + s}]<{2 * s}")

    for idx in range(38):
        total = idx // 2 + idx % 2
        lines.append(f"[{ONES_BASE + idx}]<{total % 10}")
        lines.append(f"[{CARRY_BASE + idx}]<{total // 10}")

    for c in range(48, 58):
        lines.append(f"[{DIGIT_BASE + c}]<{c - 48}")

    for d in range(10):
        lines.append(f"[{ASCII_BASE + d}]<{48 + d}")

    lines.append(f"[{ASCII_FIRST_BASE}]<0")
    lines.append(f"[{ASCII_FIRST_BASE + 1}]<49")

    for i in range(10):
        lines.append("A<I")
        lines.append(f"[{ARR1 + i}]<[A+{DIGIT_BASE}]")

    lines.append("A<I")

    for i in range(10):
        lines.append("A<I")
        lines.append(f"[{ARR2 + i}]<[A+{DIGIT_BASE}]")

    lines.append(f"[{CARRY}]<0")

    for pos in range(9, -1, -1):
        lines.append(f"A<[{ARR1 + pos}]")
        lines.append(f"B<[{ARR2 + pos}]")
        lines.append(f"C<[A+{ROW10_BASE}]")
        lines.append("X<[C+B]")
        lines.append(f"D<[X+{ADD2_BASE}]")
        lines.append(f"E<[D+{ROW2_BASE}]")
        lines.append(f"F<[{CARRY}]")
        lines.append("Y<[E+F]")
        lines.append(f"R<[Y+{ONES_BASE}]")
        lines.append(f"[{CARRY}]<[Y+{CARRY_BASE}]")
        lines.append(f"[{OUT + pos + 1}]<R")

    lines.append(f"[{OUT}]<[{CARRY}]")

    lines.append(f"A<[{OUT}]")
    lines.append(f"O<[A+{ASCII_FIRST_BASE}]")
    for i in range(1, 11):
        lines.append(f"A<[{OUT + i}]")
        lines.append(f"O<[A+{ASCII_BASE}]")
    lines.append("Z<1")

    write("2281.mv", lines)


def gen_2282() -> None:
    ID_BASE = 0
    ROW10_BASE = 100
    MIN_BASE = 110
    MAX_BASE = 210
    DIGIT_BASE = 400
    ASCII_BASE = 460
    ARR = 500

    lines: list[str] = []

    for i in range(100):
        lines.append(f"[{ID_BASE + i}]<{i}")

    for d in range(10):
        lines.append(f"[{ROW10_BASE + d}]<{d * 10}")

    for a in range(10):
        for b in range(10):
            idx = a * 10 + b
            lines.append(f"[{MIN_BASE + idx}]<{min(a, b)}")
            lines.append(f"[{MAX_BASE + idx}]<{max(a, b)}")

    for c in range(48, 58):
        lines.append(f"[{DIGIT_BASE + c}]<{c - 48}")

    for d in range(10):
        lines.append(f"[{ASCII_BASE + d}]<{48 + d}")

    for i in range(5):
        lines.append("A<I")
        lines.append(f"[{ARR + i}]<[A+{DIGIT_BASE}]")

    def compswap(i: int, j: int) -> list[str]:
        return [
            f"A<[{ARR + i}]",
            f"B<[{ARR + j}]",
            f"C<[A+{ROW10_BASE}]",
            "X<[C+B]",
            f"D<[X+{MIN_BASE}]",
            f"E<[X+{MAX_BASE}]",
            f"[{ARR + i}]<D",
            f"[{ARR + j}]<E",
        ]

    network = [
        (0, 1),
        (3, 4),
        (2, 4),
        (2, 3),
        (1, 4),
        (0, 3),
        (0, 2),
        (1, 3),
        (1, 2),
    ]

    for i, j in network:
        lines.extend(compswap(i, j))

    for i in range(5):
        lines.append(f"A<[{ARR + i}]")
        lines.append(f"O<[A+{ASCII_BASE}]")

    lines.append("Z<1")
    write("2282.mv", lines)


def hanoi_moves(n: int, a: str, b: str, c: str, out: list[str]) -> None:
    if n == 0:
        return
    hanoi_moves(n - 1, a, c, b, out)
    out.append(f"{a}->{c}\n")
    hanoi_moves(n - 1, b, a, c, out)


def gen_2283() -> None:
    # Full support for n = 1..10 using columnar char table.
    CONV_BASE = 0
    CHAR_BASE = 1000

    strings: list[str] = []
    for n in range(1, 11):
        out: list[str] = []
        hanoi_moves(n, "A", "B", "C", out)
        strings.append("".join(out))

    max_len = max(len(s) for s in strings)
    width = 10

    lines: list[str] = []

    for c in range(49, 59):
        lines.append(f"[{CONV_BASE + c}]<{c - 49}")

    for pos in range(max_len):
        row_base = CHAR_BASE + pos * width
        for idx in range(width):
            ch = ord(strings[idx][pos]) if pos < len(strings[idx]) else 0
            lines.append(f"[{row_base + idx}]<{ch}")

    lines += [
        "A<I",
        f"B<[A+{CONV_BASE}]",
    ]

    for pos in range(max_len):
        lines.append(f"O<[B+{CHAR_BASE + pos * width}]")

    lines.append("Z<1")
    write("2283.mv", lines)


def main() -> None:
    gen_2276()
    gen_2277()
    gen_2278()
    gen_2279()
    gen_2280()
    gen_2281()
    gen_2282()
    gen_2283()


if __name__ == "__main__":
    main()
