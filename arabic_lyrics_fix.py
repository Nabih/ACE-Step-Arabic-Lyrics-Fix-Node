"""Arabic Lyrics Fix — a ComfyUI custom node for ACE-Step (and any lyric-driven
music model) that makes fully-vocalized fuṣḥā Arabic lyrics sing correctly.

Why it exists (empirically established, 2025-11-18):
  Music models like ACE-Step train on unvocalized Arabic lyrics, so they:
    - swallow the tanwin syllable (غِنَاءً sung 'ghina' instead of 'ghina-an')
    - drop the ta-marbuta hard-t (بَسْمَةً -> 'basman' instead of 'basmatan')
  User-verified fix: rewrite fragile spellings into bare letter forms the model
  knows from its unvocalized training data:
      دُرَّةً   -> دررتن   (shadda -> doubled letter, ة -> hard ت, tanwin -> ن)
      بَسْمَةً  -> بسمتن
      غِنَاءً  -> غناءن   (bare word-final ن is a trained word shape — survives
                          line ends, where diacritic codas die)
  Plus shadda handling:
      sun-letter assimilation:  الزَّمَانُ -> ازْزَمَانُ (lam drops: 'az-zamān')
      lexical shadda:           أُحِبُّكِ -> أُحِبْبُكِ ('uḥibbuki')

Notes:
  - results vary by seed; treat pronunciation as an artistic choice
    (يحق للشاعر ما لا يحق لغيره)
  - use per-word overrides for stubborn cases

Your lyrics file stays literary/intact — this node outputs the model-friendly
version and you wire it into the lyrics input of your music node.
"""

import re

# diacritics that are NOT shadda/sukun (used in "haraka" slots)
_HARAKAT = "\u064B\u064C\u064D\u064E\u064F\u0650"
_ANY_DIAC = "\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0640\u0670"
_TANWIN = "\u064B\u064C\u064D"
_LETTER = "\u0621-\u064A\u0640"

_SUN = "\u062A\u062B\u062F\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0644\u0646"


def _normalize_order(text):
    """shadda-after-tanwin -> shadda-before-tanwin (canonical order)."""
    return re.sub("([" + _TANWIN + "])\u0651", lambda m: "\u0651" + m.group(1), text)


def _bare_word(word):
    """Model-friendly spelling: strip harakat EXCEPT the first letter's vowel
    (the model otherwise guesses it — ghinā'an sang as 'ghāna'), double shadda
    letters, hard-te the ta marbuta. (Caller appends the tanwin noon.)"""
    out = []
    kept_vowel = False
    for ch in word:
        if ch == "\u0651":
            if out:
                out.append(out[-1])          # shadda -> doubled letter
        elif ch in _ANY_DIAC:
            if not kept_vowel:
                out.append(ch)               # first vowel = hint the model needs
                kept_vowel = True
            continue                          # later harakat stripped
        elif ch == "\u0629":
            out.append("\u062A")              # ة -> hard ت
        else:
            out.append(ch)
    return "".join(out)


def transform_arabic_lyrics(text, overrides=None):
    """Apply all user-verified transforms. `overrides`: dict 'source' -> 'replacement'
    applied verbatim at the end (for stubborn words)."""
    if overrides is None:
        overrides = {}

    text = _normalize_order(text)

    # 1) ANY word ending in tanwin -> bare spelling + hard noon.
    #    (blob = letters + harakat/sukun/shadda, ending with a tanwin mark)
    def _tanwin_bare(m):
        return _bare_word(m.group(0)) + "\u0646"
    text = re.sub("[" + _LETTER + "][" + _LETTER + _ANY_DIAC + "]*[" + _TANWIN + "]",
                  _tanwin_bare, text)

    # 2a) sun-letter assimilation: ال + sun letter + shadda -> lam drops, letter doubles
    #     (الزَّمَانُ = az-zamān, NOT al-zzamān)
    text = re.sub("\u0627\u0644[" + _HARAKAT + "]*([" + _SUN + "])([" + _HARAKAT + "]*)\u0651([" + _HARAKAT + "]*)",
                  lambda m: "\u0627" + m.group(1) + "\u0652" + m.group(1) + (m.group(2) or "") + (m.group(3) or ""),
                  text)

    # 2b) lexical shadda -> doubled letters (أُحِبُّكِ -> أُحِبْبُكِ 'uḥibbuki')
    text = re.sub("([" + _LETTER + "])([" + _HARAKAT + "]*)\u0651([" + _HARAKAT + "]*)",
                  lambda m: m.group(1) + "\u0652" + m.group(1) + (m.group(2) or "") + (m.group(3) or ""),
                  text)

    # 3) per-song overrides (verbatim)
    for src, dst in (overrides or {}).items():
        text = text.replace(src, dst)

    return text


def parse_overrides(text):
    """Parse override lines:  'source => replacement' (one per line)."""
    out = {}
    for ln in (text or "").splitlines():
        s = ln.strip()
        if not s or "=>" not in s:
            continue
        a, b = s.split("=>", 1)
        if a.strip() and b.strip():
            out[a.strip()] = b.strip()
    return out


class ArabicLyricsFix:
    """Rewrites vocalized Arabic lyrics into model-friendly spellings.
    Wire its output into the lyrics input of ACE-Step (or any music node)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lyrics": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Literary Arabic lyrics, ideally with full harakat "
                               "(tashkeel). Stay intact — this node does not modify "
                               "your file, only its output.",
                }),
                "language": (["ar", "pass-through"], {
                    "default": "ar",
                    "tooltip": "'ar' applies the transforms; 'pass-through' returns "
                               "the input unchanged (for non-Arabic songs).",
                }),
                "overrides": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Per-word fixes, one per line:  source => replacement\n"
                               "e.g.  الرَّدُّ => الرَّدْدُ",
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("lyrics_fixed",)
    FUNCTION = "fix"
    CATEGORY = "ToneTaste/text"

    def fix(self, lyrics, language, overrides):
        if language == "pass-through":
            return (lyrics,)
        return (transform_arabic_lyrics(lyrics, parse_overrides(overrides)),)


class ArabicLyricsPreview:
    """Debug helper: shows the transformed output as text you can inspect/save."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"lyrics_fixed": ("STRING", {"multiline": True, "forceInput": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "show"
    OUTPUT_NODE = True
    CATEGORY = "ToneTaste/text"

    def show(self, lyrics_fixed):
        print("[ArabicLyricsPreview]\n" + lyrics_fixed)
        return {"ui": {"text": lyrics_fixed}, "result": (lyrics_fixed,)}


NODE_CLASS_MAPPINGS = {
    "ArabicLyricsFix": ArabicLyricsFix,
    "ArabicLyricsPreview": ArabicLyricsPreview,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ArabicLyricsFix": "Arabic Lyrics Fix (fuṣḥā)",
    "ArabicLyricsPreview": "Arabic Lyrics Preview",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "transform_arabic_lyrics"]
