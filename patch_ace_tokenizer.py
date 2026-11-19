#!/usr/bin/env python3
"""Optional patcher: makes ACE-Step's own lyric tokenizer tanwin-safe.

The node-level transform (arabic_lyrics_fix.py) already rewrites fragile
spellings into bare forms, which is enough. This patch is a belt-and-suspenders
addition: inside ACE-Step's tokenizer it expands any tanwin diacritic that
survives user workflows into phonetic letters (ـً -> ـَنْ etc.), so even
hand-fed vocalized lyrics sing their tanwin.

Idempotent: safe to run multiple times (detects the marker and skips).
Usage:
    python patch_ace_tokenizer.py --ace-path /path/to/ace-step
It backs up the original file as lyric_tokenizer.py.orig the first time.
"""
import argparse, os, re, sys

MARKER = "ARABIC_TANWIN_EXPAND_V1"
FUNC = '''
def arabic_tanwin_expand_{marker}(text):
    """ACE undertrains tanwin diacritic tokens; expand to phonetic letters:
    ـً -> ـَنْ (fathatan), ـٍ -> ـِنْ (kasratan), ـٌ -> ـُنْ (dammatan).
    ة+tanwin is pronounced with hard ت: بَسْمَةً -> بَسْمَتَنْ."""
    text = text.replace("\\u0629\\u064B", "\\u062A\\u064E\\u0646\\u0652")
    text = text.replace("\\u0629\\u064D", "\\u062A\\u0650\\u0646\\u0652")
    text = text.replace("\\u0629\\u064C", "\\u062A\\u064F\\u0646\\u0652")
    text = text.replace("\\u064B", "\\u064E\\u0646\\u0652")
    text = text.replace("\\u064D", "\\u0650\\u0646\\u0652")
    text = text.replace("\\u064C", "\\u064F\\u0646\\u0652")
    return text

'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ace-path", required=True,
                    help="path to the ace-step repo (containing acestep/)")
    args = ap.parse_args()

    target = os.path.join(args.ace_path, "acestep", "models", "lyrics_utils",
                          "lyric_tokenizer.py")
    if not os.path.exists(target):
        sys.exit(f"not found: {target}")

    src = open(target, encoding="utf-8").read()
    if MARKER in src:
        print("already patched — nothing to do")
        return

    orig = target + ".orig"
    if not os.path.exists(orig):
        open(orig, "w", encoding="utf-8").write(src)
        print(f"backup written: {orig}")

    marker = MARKER.lower()
    # 1) insert the function before multilingual_cleaners
    anchor = "def multilingual_cleaners(text, lang):"
    if anchor not in src:
        sys.exit("anchor function not found — ACE version mismatch?")
    fn_code = "# MARKER: " + MARKER + "\n" + FUNC.replace("{marker}", marker)
    src = src.replace(anchor, fn_code + anchor, 1)

    # 2) hook the call inside multilingual_cleaners' body (robust: operate on the
    #    function slice, replace its "text = collapse_whitespace(text)" line)
    start = src.index(anchor)
    nxt = src.find("\ndef ", start + 1)
    body = src[start:nxt]
    needle = "    text = collapse_whitespace(text)"
    if needle not in body:
        sys.exit("collapse_whitespace call not found in multilingual_cleaners")
    hook = (needle + "\n"
            "    if lang == \"ar\":\n"
            f"        text = arabic_tanwin_expand_{marker}(text)")
    body = body.replace(needle, hook, 1)
    src = src[:start] + body + src[nxt:]

    open(target, "w", encoding="utf-8").write(src)
    print(f"patched: {target} (marker {MARKER})")

if __name__ == "__main__":
    main()
