# Word uchun O‘zbek alifbosi konvertori (add-in)

Word'ning yuqori menyusida **Konvertor** bo‘limi paydo bo‘ladi:

- **Konvertor paneli**: yon panelda yozuvlarni tanlab, tanlangan matn yoki butun hujjatni almashtiradi.
- **Tez almashtirish**: bir bosishda 6 ta yo‘nalish (eski lotin, yangi lotin, kirill, o‘zaro).

Tanlangan matn bo‘lmasa, butun hujjat almashtiriladi. Formatlash (qalin, kursiv, o‘lcham) saqlanadi. Natijani Ctrl+Z bilan qaytarish mumkin.

## O‘rnatish

1. GitHub Pages yoqilgan bo‘lishi kerak: repozitoriyda **Settings → Pages → Deploy from a branch → main / (root)**.
2. `manifest.xml` faylini kompyuterga yuklab oling.
3. Word'da **Insert (Qo‘shish) → Add-ins → My Add-ins → Manage My Add-ins → Upload My Add-in** ni tanlab, `manifest.xml` ni ko‘rsating.
4. Menyuda **Konvertor** bo‘limi paydo bo‘ladi.

Word'ning eski versiyalarida (2016, 2019) shu yo‘l bo‘lmasa, manifest faylini umumiy papkaga qo‘yib, **File → Options → Trust Center → Trusted Add-in Catalogs** orqali papka manzilini qo‘shing, so‘ng **Insert → My Add-ins → Shared Folder** dan tanlang.
