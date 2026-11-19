# Audio embed test — absolute URLs
# اختبار تضمين الصوت — روابط مطلقة

## Variant 1 — `<video controls>` with absolute raw URL
## الصيغة 1 — وسم video مع رابط مطلق

| | Without the node | With the node |
|---|---|---|
| عَنْ عَيْنَيْكِ كَتَبَ الْبَحْرُ غِنَاءً | <video controls width="320" src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/before_ghinaan.mp4"></video> | <video controls width="320" src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/after_ghinaan.mp4"></video> |
| يَا بَسْمَةً | <video controls width="320" src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/before_basmatan.mp4"></video> | <video controls width="320" src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/after_basmatan.mp4"></video> |

---

## Variant 2 — `<audio controls>` with absolute raw URL
## الصيغة 2 — وسم audio مع رابط مطلق

<audio controls src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/before_ghinaan.mp3"></audio> — without the node / بدون العقدة
<audio controls src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/after_ghinaan.mp3"></audio> — with the node / مع العقدة
<audio controls src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/before_basmatan.mp3"></audio> — without the node / بدون العقدة
<audio controls src="https://raw.githubusercontent.com/Nabih/ACE-Step-Arabic-Lyrics-Fix-Node/master/assets/after_basmatan.mp3"></audio> — with the node / مع العقدة

---

## Variant 3 — relative URL for comparison (expected to fail)
## الصيغة 3 — رابط نسبي للمقارنة (متوقع الفشل)

| | Without the node | With the node |
|---|---|---|
| عَنْ عَيْنَيْكِ كَتَبَ الْبَحْرُ غِنَاءً | <video controls width="320" src="assets/before_ghinaan.mp4"></video> | <video controls width="320" src="assets/after_ghinaan.mp4"></video> |
