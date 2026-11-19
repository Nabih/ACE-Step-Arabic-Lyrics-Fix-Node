# Arabic Lyrics Fix — ComfyUI custom node

Makes fully-vocalized fuṣḥā Arabic lyrics **sing correctly** in ACE-Step (and any
lyric-driven music node). Built and user-verified on the song «أحبُّكِ» (2025-11-18).

## The problem

Music models train on **unvocalized** Arabic lyrics, so fully-vocalized input gets
mangled: the tanwin is swallowed (غِنَاءً sung "ghina" instead of "ghinā'an"), the
ta-marbuta hard-t drops (بَسْمَةً → "basman"), gemination is flaky, and fragile
spellings break worst at line ends and in short lines.

## The fix (node-level, your lyrics stay intact)

The node rewrites fragile spellings into **bare letter forms the model knows**:

| Literary | Transformed | Sings |
|---|---|---|
| دُرَّةً | دررتن | dur-ratan |
| بَسْمَةً | بسمتن | basmatan |
| غِنَاءً | غناءن | ghinā'an (survives line ends) |
| الزَّمَانُ | ازْزَمَانُ | az-zamān (sun-letter assimilation) |
| أُحِبُّكِ | أُحِبْبُكِ | uḥibbuki (lexical shadda) |

Per-word overrides handle stubborn cases (they beat every general rule):

```
الرَّدُّ => الرَّدْدُ
```

## Install

Copy this folder into `ComfyUI/custom_nodes/`:

```
ComfyUI/custom_nodes/arabic-lyrics-fix-node/
├── __init__.py
├── arabic_lyrics_fix.py     ← the node (no dependencies)
├── patch_ace_tokenizer.py   ← optional tokenizer patcher
└── README.md
```

Restart ComfyUI. You get two nodes under **ToneTaste/text**:

- **Arabic Lyrics Fix (fuṣḥā)** — lyrics in (STRING, multiline) → transformed lyrics
  out. Wire the output into your music node's `lyrics` input. Set
  `language=pass-through` for non-Arabic songs (input returned unchanged).
- **Arabic Lyrics Preview** — debug node: shows the transformed text in the UI/console.

## Optional: patch the ACE-Step tokenizer itself

Belt-and-suspenders — expands any surviving tanwin diacritic inside ACE-Step:

```
python patch_ace_tokenizer.py --ace-path /path/to/ace-step
```

Idempotent; backs up the original as `lyric_tokenizer.py.orig`.

## Lyrics-writing conventions (verified)

- Full harakat everywhere — mid-word vowels sing correctly
- Tanwin words: converted automatically; they sing best mid-phrase
- Shadda: handled via doubling; if a specific word deserves its gemination,
  route it through the overrides box
- Case endings and gemination vary from take to take — treat them as
  artistic choices (يحق للشاعر ما لا يحق لغيره)
- For stubborn words, use the overrides box instead of editing your lyrics file
