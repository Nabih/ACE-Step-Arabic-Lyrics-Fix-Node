# Arabic Lyrics Fix — ComfyUI custom node
# مصلّح الكلمات العربية — عقدة (Node) إضافة لـ ComfyUI

Makes fully-vocalized fuṣḥā Arabic lyrics **sing correctly** in ACE-Step (and any
lyric-driven music node). Built and user-verified on the song «أحبُّكِ» (2025-11-18).

يجعل كلمات الفصحى المُشكَّلة بالكامل **تُغنَّى بشكل صحيح** في ACE-Step (وأي عقدة موسيقية
تعتمد على الكلمات). بُني وتم التحقق منه على أغنية «أحبُّكِ» (2025-11-18).

> 💬 Any comments or suggestions are welcome!
> 💬 أي ملاحظات أو اقتراحات مرحب بها دائماً!

## The problem
## المشكلة

Music models train on **unvocalized** Arabic lyrics, so fully-vocalized input gets
mangled: the tanwin is swallowed (غِنَاءً sung "ghina" instead of "ghinā'an"), the
ta-marbuta hard-t drops (بَسْمَةً → "basman"), gemination is flaky, and fragile
spellings break worst at line ends and in short lines.

تتدرَّب النماذج الموسيقية على كلمات عربية **غير مُشكَّلة**، لذلك تُشوَّه الكلمات
المُشكَّلة بالكامل: يُبتلَع التنوين (غِنَاءً تُغنَّى "ghina" بدل "ghinā'an")، ويَسقُط
تاء التأنيث الساكنة (بَسْمَةً → "basman")، ويصبح التضعيف متذبذباً، وتنكسر الألفاظ
الهشّة أكثر عند نهايات الأسطر وفي الأسطر القصيرة.

## The fix (node-level, your lyrics stay intact)
## الحل (على مستوى العقدة — ملف كلماتك يبقى كما هو سليماً)

The node rewrites fragile spellings into **bare letter forms the model knows**:

تعيد العقدة كتابة الألفاظ الهشّة إلى **أشكال حرفية مجرَّدة يعرفها النموذج**:

| Literary | Transformed | Sings |
|---|---|---|
| الأصلية | المُحوَّلة | تُغنَّى |
| دُرَّةً | دررتن | dur-ratan |
| بَسْمَةً | بسمتن | basmatan |
| غِنَاءً | غناءن | ghinā'an (survives line ends) |
| الزَّمَانُ | ازْزَمَانُ | az-zamān (sun-letter assimilation) |
| أُحِبُّكِ | أُحِبْبُكِ | uḥibbuki (lexical shadda) |

Per-word overrides handle stubborn cases (they beat every general rule):

معالجات لكل كلمة على حدة للحالات العنيدة (وتتغلَّب على كل قاعدة عامة):

```
الرَّدُّ => الرَّدْدُ
```

## Install
## التثبيت

Copy this folder into `ComfyUI/custom_nodes/`:

انسخ هذا المجلد إلى `ComfyUI/custom_nodes/`:

```
ComfyUI/custom_nodes/arabic-lyrics-fix-node/
├── __init__.py
├── arabic_lyrics_fix.py     ← the node (no dependencies) — العقدة (بدون أي اعتماديات)
├── patch_ace_tokenizer.py   ← optional tokenizer patcher — مُرقّع المُقسِّم الاختياري
└── README.md
```

Restart ComfyUI. You get two nodes under **ToneTaste/text**:

أعد تشغيل ComfyUI. ستحصل على عقدتين تحت **ToneTaste/text**:

- **Arabic Lyrics Fix (fuṣḥā)** — lyrics in (STRING, multiline) → transformed lyrics
  out. Wire the output into your music node's `lyrics` input. Set
  `language=pass-through` for non-Arabic songs (input returned unchanged).
- **Arabic Lyrics Fix (فصحى)** — الكلمات دخل (STRING متعدد الأسطر) → الكلمات
  المحوَّلة خرج. صِل الخرج بمدخل `lyrics` في عقدتك الموسيقية. اجعل
  `language=pass-through` للأغاني غير العربية (يعود الدخل دون تغيير).
- **Arabic Lyrics Preview** — debug node: shows the transformed text in the UI/console.
- **معاينة الكلمات العربية** — عقدة فحص: تعرض النص المحوَّل في الواجهة/وحدة التحكم.

## Optional: patch the ACE-Step tokenizer itself
## اختياري: ترقيع مُقسِّم الكلمات في ACE-Step نفسه

Belt-and-suspenders — expands any surviving tanwin diacritic inside ACE-Step:

حزام وأمان — يوسِّع أي تنوين باقٍ داخل ACE-Step:

```
python patch_ace_tokenizer.py --ace-path /path/to/ace-step
```

Idempotent; backs up the original as `lyric_tokenizer.py.orig`.

قابل للتكرار بأمان؛ يحفظ نسخة من الملف الأصلي باسم `lyric_tokenizer.py.orig`.

## Lyrics-writing conventions (verified)
## قواعد كتابة الكلمات (مُتحقَّق منها عملياً)

- Full harakat everywhere — mid-word vowels sing correctly
- الحركات الكاملة في كل مكان — حروف المد داخل الكلمة تُغنَّى بشكل صحيح
- Tanwin words: converted automatically; they sing best mid-phrase
- كلمات التنوين: تُحوَّل تلقائياً؛ وتُغنَّى بأفضل شكل في وسط العبارة
- Shadda: handled via doubling; if a specific word deserves its gemination,
  route it through the overrides box
- الشدّة: تُعالَج بالتضعيف؛ وإذا استحقّت كلمةٌ معيّنة تضعيفها،
  وجِّهها عبر صندوق المعالجات
- Case endings and gemination vary from take to take — treat them as
  artistic choices (يحق للشاعر ما لا يحق لغيره)
- الحركات الإعرابية والتضعيف تختلف من أداء لآخر — اعتبرها خيارات فنية
  (يحق للشاعر ما لا يحق لغيره)
- For stubborn words, use the overrides box instead of editing your lyrics file
- للحالات العنيدة، استخدم صندوق المعالجات بدل تعديل ملف كلماتك

## License
## الرخصة

MIT
