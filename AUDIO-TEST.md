# Audio embed test — MP4 inline players
# اختبار تضمين الصوت — مشغّلات MP4 مضمّنة

## Variant 1 — `<video controls>`
## الصيغة 1 — وسم `<video controls>`

| | Without the node | With the node |
|---|---|---|
| عَنْ عَيْنَيْكِ كَتَبَ الْبَحْرُ غِنَاءً | <video controls width="320" src="assets/before_ghinaan.mp4"></video> | <video controls width="320" src="assets/after_ghinaan.mp4"></video> |
| يَا بَسْمَةً | <video controls width="320" src="assets/before_basmatan.mp4"></video> | <video controls width="320" src="assets/after_basmatan.mp4"></video> |

---

## Variant 2 — `<video controls>` + poster text fallback
## الصيغة 2 — وسم video مع نص بديل

<video controls width="320" src="assets/before_ghinaan.mp4">
  غِنَاءً swallowed — fallback link: [assets/before_ghinaan.mp4](assets/before_ghinaan.mp4)
</video>

<video controls width="320" src="assets/after_ghinaan.mp4">
  غِنَاءً sung — fallback link: [assets/after_ghinaan.mp4](assets/after_ghinaan.mp4)
</video>

---

## Variant 3 — plain markdown links to the mp4s (GitHub renders these with a player when clicked)
## الصيغة 3 — روابط مباشرة (يفتحها GitHub بمشغّل عند الضغط)

- [غِنَاءً — without the node / بدون العقدة](assets/before_ghinaan.mp4)
- [غِنَاءً — with the node / مع العقدة](assets/after_ghinaan.mp4)
- [بَسْمَةً — without the node / بدون العقدة](assets/before_basmatan.mp4)
- [بَسْمَةً — with the node / مع العقدة](assets/after_basmatan.mp4)
