# Arabic Lyrics Fix — ComfyUI custom node for ACE-Step
# [مصلّح الكلمات العربية](#العربية) — عقدة (Node) إضافة لـ ComfyUI لأجل ACE-Step

> 💬 Any comments or suggestions are welcome!
> 💬 أي ملاحظات أو اقتراحات مرحب بها دائماً!

---

## English

Makes fully-vocalized fuṣḥā Arabic lyrics **sing correctly** in
[ACE-Step](https://acestep.io/) (verified on **ACE-Step v1.5**, checkpoint
[`acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo);
other v1.5 checkpoints on Hugging Face:
[sft](https://huggingface.co/ACE-Step/acestep-v15-xl-sft),
[base](https://huggingface.co/ACE-Step/acestep-v15-xl-base)). The transform is
pure text preprocessing and may help other Arabic-lyric music models too
(untested). A step-by-step guide lives in [TUTORIAL.md](TUTORIAL.md).

### The problem

Music models train on **unvocalized** Arabic lyrics, so fully-vocalized input gets
mangled: the tanwin is swallowed (غِنَاءً sung "ghina" instead of "ghinā'an"), the
ta-marbuta hard-t drops (بَسْمَةً → "basman"), gemination is flaky, and fragile
spellings break worst at line ends and in short lines.

### The fix (node-level, your lyrics stay intact)

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

### Install

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

### Optional: patch the ACE-Step tokenizer itself

Belt-and-suspenders — expands any surviving tanwin diacritic inside ACE-Step:

```
python patch_ace_tokenizer.py --ace-path /path/to/ace-step
```

Idempotent; backs up the original as `lyric_tokenizer.py.orig`.

### Lyrics-writing conventions (verified)

- Full harakat everywhere — mid-word vowels sing correctly
- Tanwin words: converted automatically; they sing best mid-phrase
- Shadda: handled via doubling; if a specific word deserves its gemination,
  route it through the overrides box
- Case endings and gemination vary from take to take — treat them as
  artistic choices (يحق للشاعر ما لا يحق لغيره)
- For stubborn words, use the overrides box instead of editing your lyrics file

### License

MIT

---

## العربية

يجعل كلمات الفصحى المُشكَّلة بالكامل **تُغنَّى بشكل صحيح** في
[ACE-Step](https://acestep.io/) (مُتحقَّق عليه على **ACE-Step v1.5** بنموذج
[`acestep-v15-xl-turbo`](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo)؛
النماذج الأخرى على Hugging Face:
[sft](https://huggingface.co/ACE-Step/acestep-v15-xl-sft)،
[base](https://huggingface.co/ACE-Step/acestep-v15-xl-base)). التحوّل نصي بحت وقد
يفيد نماذج موسيقية عربية أخرى أيضاً — غير مُختبَر عليها بعد. للاطلاع على شرح
خطوة بخطوة انظر [TUTORIAL.md](TUTORIAL.md).

### المشكلة

تتدرَّب النماذج الموسيقية على كلمات عربية **غير مُشكَّلة**، لذلك تُشوَّه الكلمات
المُشكَّلة بالكامل: يُبتلَع التنوين (غِنَاءً تُغنَّى "ghina" بدل "ghinā'an")، ويَسقُط
تاء التأنيث الساكنة (بَسْمَةً → "basman")، ويصبح التضعيف متذبذباً، وتنكسر الألفاظ
الهشّة أكثر عند نهايات الأسطر وفي الأسطر القصيرة.

### الحل (على مستوى العقدة — ملف كلماتك يبقى كما هو سليماً)

تعيد العقدة كتابة الألفاظ الهشّة إلى **أشكال حرفية مجرَّدة يعرفها النموذج**:

| الأصلية | المُحوَّلة | تُغنَّى |
|---|---|---|
| دُرَّةً | دررتن | dur-ratan |
| بَسْمَةً | بسمتن | basmatan |
| غِنَاءً | غناءن | ghinā'an (تصمد عند نهايات الأسطر) |
| الزَّمَانُ | ازْزَمَانُ | az-zamān (إدغام الحروف الشمسية) |
| أُحِبُّكِ | أُحِبْبُكِ | uḥibbuki (شدّة معجمية) |

معالجات لكل كلمة على حدة للحالات العنيدة (وتتغلَّب على كل قاعدة عامة):

```
الرَّدُّ => الرَّدْدُ
```

### التثبيت

انسخ هذا المجلد إلى `ComfyUI/custom_nodes/`:

```
ComfyUI/custom_nodes/arabic-lyrics-fix-node/
├── __init__.py
├── arabic_lyrics_fix.py     ← العقدة (بدون أي اعتماديات)
├── patch_ace_tokenizer.py   ← مُرقّع المُقسِّم الاختياري
└── README.md
```

أعد تشغيل ComfyUI. ستحصل على عقدتين تحت **ToneTaste/text**:

- **Arabic Lyrics Fix (فصحى)** — الكلمات دخل (STRING متعدد الأسطر) → الكلمات المحوَّلة
  خرج. صِل الخرج بمدخل `lyrics` في عقدتك الموسيقية. اجعل `language=pass-through`
  للأغاني غير العربية (يعود الدخل دون تغيير).
- **معاينة الكلمات العربية** — عقدة فحص: تعرض النص المحوَّل في الواجهة/وحدة التحكم.

### اختياري: ترقيع مُقسِّم الكلمات في ACE-Step نفسه

حزام وأمان — يوسِّع أي تنوين باقٍ داخل ACE-Step:

```
python patch_ace_tokenizer.py --ace-path /path/to/ace-step
```

قابل للتكرار بأمان؛ يحفظ نسخة من الملف الأصلي باسم `lyric_tokenizer.py.orig`.

### قواعد كتابة الكلمات (مُتحقَّق منها عملياً)

- الحركات الكاملة في كل مكان — حروف المد داخل الكلمة تُغنَّى بشكل صحيح
- كلمات التنوين: تُحوَّل تلقائياً؛ وتُغنَّى بأفضل شكل في وسط العبارة
- الشدّة: تُعالَج بالتضعيف؛ وإذا استحقّت كلمةٌ معيّنة تضعيفها،
  وجِّهها عبر صندوق المعالجات
- الحركات الإعرابية والتضعيف تختلف من أداء لآخر — اعتبرها خيارات فنية
  (يحق للشاعر ما لا يحق لغيره)
- للحالات العنيدة، استخدم صندوق المعالجات بدل تعديل ملف كلماتك

### الرخصة

MIT
