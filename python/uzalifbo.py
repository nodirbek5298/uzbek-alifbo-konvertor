#!/usr/bin/env python3
"""
uzalifbo.py: o‘zbek alifbosi konvertori (ommaviy fayl konvertatsiyasi)

Yozuvlar:  eski  = eski lotin (O‘, G‘, Sh, Ch)
           yangi = yangi lotin (Ö, Ğ, Ş, Ç)
           kirill = kirill

Misollar:
  python uzalifbo.py hujjatlar --dan eski --ga yangi
  python uzalifbo.py hujjatlar --dan kirill --ga yangi --rekursiv
  python uzalifbo.py kitob.docx --dan eski --ga kirill
  python uzalifbo.py hujjatlar --dan eski --ga yangi --ichida

Qo‘llab-quvvatlanadigan fayllar: .txt .md .csv .srt .html .json .docx
Muallif: Nodirbek Qalandarov (@nodir691)
"""
import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

APOS = "'‘’ʻʼ`´′"
TEXT_EXT = {".txt", ".md", ".csv", ".srt", ".html", ".json"}

# ---------- eski lotin <-> yangi lotin ----------
_NEW = {"O": "Ö", "o": "ö", "G": "Ğ", "g": "ğ"}
_OLD = {"Ö": "O‘", "ö": "o‘", "Ğ": "G‘", "ğ": "g‘",
        "Ş": "Sh", "ş": "sh", "Ç": "Ch", "ç": "ch"}


def old_to_new(s: str) -> str:
    s = re.sub("([OoGg])[" + APOS + "]", lambda m: _NEW[m.group(1)], s)
    s = re.sub("([Ss])[Hh]", lambda m: "Ş" if m.group(1) == "S" else "ş", s)
    s = re.sub("([Cc])[Hh]", lambda m: "Ç" if m.group(1) == "C" else "ç", s)
    return s


def new_to_old(s: str) -> str:
    return re.sub("[ÖöĞğŞşÇç]", lambda m: _OLD[m.group(0)], s)


# ---------- kirill <-> eski lotin ----------
CYR = "А-Яа-яЁёЎўҚқҒғҲҳ"
_CYR_RE = re.compile("[" + CYR + "]")
_VOWELS = set("аеёиоуўэюяыАЕЁИОУЎЭЮЯЫ")
_C2L = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ж": "j", "з": "z",
    "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x",
    "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "’", "ь": "",
    "ы": "i", "э": "e", "ю": "yu", "я": "ya", "ё": "yo", "ў": "o‘",
    "қ": "q", "ғ": "g‘", "ҳ": "h", "е": "e",
}
_L2C = {
    "a": "а", "b": "б", "d": "д", "f": "ф", "g": "г", "h": "ҳ", "i": "и",
    "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п",
    "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "x": "х",
    "y": "й", "z": "з",
}


def _cap(m: str, allcaps: bool) -> str:
    return m.upper() if allcaps else m[0].upper() + m[1:]


def cyr_to_old(s: str) -> str:
    out = []
    for i, c in enumerate(s):
        if not _CYR_RE.match(c):
            out.append(c)
            continue
        l = c.lower()
        p = s[i - 1] if i > 0 else ""
        n = s[i + 1] if i + 1 < len(s) else ""
        m = _C2L[l]
        if l == "е":
            m = "ye" if (not p or not _CYR_RE.match(p) or p in _VOWELS) else "e"
        if l == "ц" and (not p or not _CYR_RE.match(p)):
            m = "s"
        if not c.isupper() or not m:
            out.append(m)
            continue
        allcaps = len(m) > 1 and (
            (n and _CYR_RE.match(n) and n.isupper())
            or (p and _CYR_RE.match(p) and p.isupper()))
        out.append(_cap(m, allcaps))
    return "".join(out)


def _is_apos(c: str) -> bool:
    return bool(c) and c in APOS


def old_to_cyr(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        c = s[i]
        l = c.lower()
        n = s[i + 1] if i + 1 < len(s) else ""
        nl = n.lower()
        m, ln = None, 1
        if l in "og" and _is_apos(n):
            m, ln = ("ў" if l == "o" else "ғ"), 2
        elif l == "s" and nl == "h":
            m, ln = "ш", 2
        elif l == "c" and nl == "h":
            m, ln = "ч", 2
        elif l == "t" and nl == "s":
            m, ln = "ц", 2
        elif (l == "y" and nl and nl in "ouae"
              and not (nl == "o" and _is_apos(s[i + 2:i + 3]))):
            m, ln = {"o": "ё", "u": "ю", "a": "я", "e": "е"}[nl], 2
        elif _is_apos(c):
            m = "ъ"
        elif l == "e":
            prev = s[i - 1] if i > 0 else ""
            m = "е" if (i and (prev.isascii() and prev.isalpha() or _is_apos(prev))) else "э"
        else:
            m = _L2C.get(l)
        if not m:
            out.append(c)
            i += 1
            continue
        if c.isupper():
            m = _cap(m, ln == 2 and n.isupper() and len(m) > 1)
        out.append(m)
        i += ln
    return "".join(out)


# ---------- umumiy ----------
ALIASES = {"eski": "old", "yangi": "new", "kirill": "cyr"}
TO_OLD = {"old": lambda s: s, "new": new_to_old, "cyr": cyr_to_old}
FROM_OLD = {"old": lambda s: s, "new": old_to_new, "cyr": old_to_cyr}


def convert(s: str, src: str, dst: str) -> str:
    """src/dst: 'old' | 'new' | 'cyr'"""
    if src == dst:
        return s
    return FROM_OLD[dst](TO_OLD[src](s))


# ---------- fayllar ----------
_WT = re.compile(r"(<w:t(?:\s[^>]*)?>)([^<]*)(</w:t>)")
_DOCX_PART = re.compile(r"^word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$")


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "cp1251"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("kodlashni aniqlab bo‘lmadi")


def convert_docx(src_path: Path, dst_path: Path, src: str, dst: str) -> None:
    def fix(m):
        t = re.sub(r"&apos;|&#39;|&#x27;", "'", m.group(2))
        return m.group(1) + convert(t, src, dst) + m.group(3)

    with zipfile.ZipFile(src_path) as zin, \
            zipfile.ZipFile(dst_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if _DOCX_PART.match(item.filename):
                data = _WT.sub(fix, data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)


def process(path: Path, out: Path, src: str, dst: str) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".docx":
        convert_docx(path, out, src, dst)
    else:
        out.write_text(convert(read_text(path), src, dst), encoding="utf-8")
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="O‘zbek alifbosi konvertori: eski lotin, yangi lotin, kirill.")
    ap.add_argument("yol", help="fayl yoki papka")
    ap.add_argument("-d", "--dan", required=True, choices=ALIASES, help="qaysi yozuvdan")
    ap.add_argument("-g", "--ga", required=True, choices=ALIASES, help="qaysi yozuvga")
    ap.add_argument("-r", "--rekursiv", action="store_true", help="ichki papkalarni ham")
    ap.add_argument("-i", "--ichida", action="store_true",
                    help="asl fayllarni almashtirish (zaxira nusxa .bak bilan)")
    ap.add_argument("--zaxirasiz", action="store_true", help="--ichida bilan .bak yaratilmasin")
    a = ap.parse_args(argv)

    src, dst = ALIASES[a.dan], ALIASES[a.ga]
    root = Path(a.yol).resolve()
    if not root.exists():
        print("Topilmadi:", root, file=sys.stderr)
        return 1
    if src == dst:
        print("Ikkala yozuv bir xil.", file=sys.stderr)
        return 1

    if root.is_file():
        files, base = [root], root.parent
    else:
        it = root.rglob("*") if a.rekursiv else root.glob("*")
        files, base = sorted(p for p in it if p.is_file()), root
    suffix = "-" + a.ga
    outdir = None if root.is_file() or a.ichida else root.with_name(root.name + suffix)

    done = skipped = failed = 0
    for f in files:
        ext = f.suffix.lower()
        if ext not in TEXT_EXT and ext != ".docx":
            skipped += 1
            continue
        if outdir is not None and (outdir == f or outdir in f.parents):
            continue
        if a.ichida:
            if not a.zaxirasiz:
                shutil.copy2(f, f.with_name(f.name + ".bak"))
            tmp = f.with_name(f.name + ".tmp")
            target = f
        elif root.is_file():
            target = f.with_name(f.stem + suffix + f.suffix)
            tmp = None
        else:
            target = outdir / f.relative_to(base)
            tmp = None
        try:
            if tmp is not None:
                process(f, tmp, src, dst)
                tmp.replace(target)
            else:
                process(f, target, src, dst)
            done += 1
            print("✓", f)
        except Exception as e:  # noqa: BLE001
            failed += 1
            if tmp is not None and tmp.exists():
                tmp.unlink()
            print("✗", f, "-", e, file=sys.stderr)

    print(f"\nTayyor: {done} ta fayl, o‘tkazib yuborildi: {skipped}, xato: {failed}")
    if outdir is not None and done:
        print("Natija papkasi:", outdir)
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
