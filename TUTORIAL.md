# Tutorial — Singing fuṣḥā Arabic lyrics correctly with ACE-Step

# دليل عملي — غناء كلمات الفصحى العربية بشكل صحيح مع ACE-Step

> 💬 Any comments or suggestions are welcome!
> 💬 أي ملاحظات أو اقتراحات مرحب بها دائماً!

---

## English

### What you need

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) with an
  [ACE-Step](https://acestep.io/) node pack
  (models on Hugging Face: [Ace-Step1.5](https://huggingface.co/ACE-Step/Ace-Step1.5),
  [acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo),
  [acestep-v15-xl-sft](https://huggingface.co/ACE-Step/acestep-v15-xl-sft),
  [acestep-v15-xl-base](https://huggingface.co/ACE-Step/acestep-v15-xl-base))
- This node installed in `ComfyUI/custom_nodes/` (see the main README)

### Step 1 — Write literary lyrics

Write your lyrics normally, with **full tashkeel** (harakat) everywhere. Don't
pre-cripple spellings for the model — the node does that for you.

```
عَنْ عَيْنَيْكِ كَتَبَ الْبَحْرُ غِنَاءً
وَعَنْ يَدَيْكِ كَتَبَ الزَّمَانُ رِحْلَةً
```

### Step 2 — Wire the graph

```
[Lyrics text] → [Arabic Lyrics Fix] → [ACE-Step lyrics input]
```

Add the **Arabic Lyrics Fix (fuṣḥā)** node (under ToneTaste/text), paste your
lyrics into it, and connect its output to the `lyrics` input of your ACE-Step
node. Use **Arabic Lyrics Preview** to see exactly what the model will receive.

For non-Arabic songs, set `language=pass-through` — the input is returned
unchanged, so one graph works for all songs.

### Step 3 — Stubborn words? Use overrides

If one word keeps being sung the way you don't want, add an override line
instead of touching your lyrics:

```
الرَّدُّ => الرَّدْدُ
```

### Step 4 — Render and judge by ear

Results vary from take to take (seed roulette). Generate a couple of takes and
pick the one that sings the way you hear it in your head — pronunciation is an
artistic choice (يحق للشاعر ما لا يحق لغيره).

### Optional — belt and suspenders

If you also want the tokenizer itself to be tanwin-safe (for lyrics fed to
ACE-Step without the node), run the patcher once:

```
python patch_ace_tokenizer.py --ace-path /path/to/ace-step
```

### What to listen for

| Line | Without the node | With the node |
|---|---|---|
| عَنْ عَيْنَيْكِ كَتَبَ الْبَحْرُ غِنَاءً | "ghinā" (tanwin swallowed) | "ghinā'an" |
| يَا بَسْمَةً | "basma" (hard-t dropped) | "basmatan" |

---

## العربية

### ما تحتاجه

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) مع حزمة عقد
  [ACE-Step](https://acestep.io/) (النماذج على Hugging Face:
  [Ace-Step1.5](https://huggingface.co/ACE-Step/Ace-Step1.5),
  [acestep-v15-xl-turbo](https://huggingface.co/ACE-Step/acestep-v15-xl-turbo),
  [acestep-v15-xl-sft](https://huggingface.co/ACE-Step/acestep-v15-xl-sft),
  [acestep-v15-xl-base](https://huggingface.co/ACE-Step/acestep-v15-xl-base))
- هذه العقدة مثبتة في `ComfyUI/custom_nodes/` (انظر README الرئيسي)

### الخطوة 1 — اكتب كلماتك أدبيةً

اكتب كلماتك بشكل طبيعي مع **التشكيل الكامل** (الحركات) في كل مكان. لا تشوِّه
الهجاء مسبقاً اجتهاداً — العقدة تفعل ذلك عنك.

### الخطوة 2 — وصّل الرسم

```
[نص الكلمات] → [مصلّح الكلمات العربية] → [مدخل lyrics في ACE-Step]
```

أضف عقدة **Arabic Lyrics Fix (فصحى)** (تحت ToneTaste/text)، والصق كلماتك فيها،
ثم صِل خرجها بمدخل `lyrics` في عقدة ACE-Step. استخدم **معاينة الكلمات العربية**
لترى بالضبط ما سيصل إلى النموذج.

للأغاني غير العربية اجعل `language=pass-through` — يعود الدخل دون تغيير، ف يصلح
الرسم نفسه لكل الأغاني.

### الخطوة 3 — كلمة عنيدة؟ استخدم المعالجات

إذا استمرت كلمةٌ في أن تُغنَّى خلاف ما تريد، أضف سطر معالجة بدل العبث بكلماتك:

```
الرَّدُّ => الرَّدْدُ
```

### الخطوة 4 — صيِّر وحكم بأذنك

تختلف النتائج من أداء لآخر (حظ البذرة). صيِّر أداءين أو ثلاثة واختر ما يغنّى كما
تسمعه في رأسك — النطق فنٌ وقراءة (يحق للشاعر ما لا يحق لغيره).

### اختياري — حزام وأمان

إن أردت أن يكون مُقسِّم الكلمات نفسه آمناً على التنوين (لكلمات تُغذّى لـ ACE-Step
من دون العقدة)، شغّل المُرقّع مرة واحدة:

```
python patch_ace_tokenizer.py --ace-path /path/to/ace-step
```

### ما تسمعه

| السطر | بدون العقدة | مع العقدة |
|---|---|---|
| عَنْ عَيْنَيْكِ كَتَبَ الْبَحْرُ غِنَاءً | "ghinā" (تنوين مُبتلَع) | "ghinā'an" |
| يَا بَسْمَةً | "basma" (تاء ساكنة ساقطة) | "basmatan" |
