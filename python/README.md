# uzalifbo.py: fayllarni ommaviy konvertatsiya qilish

Papkadagi (yoki bitta) `.txt`, `.md`, `.csv`, `.srt`, `.html`, `.json` va `.docx` fayllarni o‘zbek alifbosining uch yozuvi o‘rtasida bir buyruq bilan almashtiradi. Faqat Python 3.8+ kerak, qo‘shimcha kutubxona o‘rnatish shart emas.

**Yozuvlar:** `eski` (eski lotin: O‘, G‘, Sh, Ch), `yangi` (yangi lotin: Ö, Ğ, Ş, Ç), `kirill`.

## Ishlatish

```bash
# papkadagi hamma fayl: eski lotin → yangi lotin (natija "hujjatlar-yangi" papkasida)
python uzalifbo.py hujjatlar --dan eski --ga yangi

# ichki papkalar bilan, kirill → yangi lotin
python uzalifbo.py hujjatlar --dan kirill --ga yangi --rekursiv

# bitta fayl (yoniga "kitob-kirill.docx" yoziladi)
python uzalifbo.py kitob.docx --dan eski --ga kirill

# asl fayllarni almashtirish (har biri uchun .bak zaxira nusxa qoladi)
python uzalifbo.py hujjatlar --dan eski --ga yangi --ichida
```

| Parametr | Ma’nosi |
|---|---|
| `-d`, `--dan` | qaysi yozuvdan (`eski`, `yangi`, `kirill`) |
| `-g`, `--ga` | qaysi yozuvga |
| `-r`, `--rekursiv` | ichki papkalarni ham ishlash |
| `-i`, `--ichida` | asl fayllarni almashtirish (`.bak` zaxira bilan) |
| `--zaxirasiz` | `--ichida` bilan zaxira nusxa yaratmaslik |

Boshqa turdagi fayllar (rasm va hokazo) o‘tkazib yuboriladi. `.docx` fayllarda formatlash saqlanadi.

## Python ichida ishlatish

```python
from uzalifbo import convert

convert("O'zbekiston, g'oya, shahar", "old", "new")   # Özbekiston, ğoya, şahar
convert("Ўзбекистон", "cyr", "new")                    # Özbekiston
```

Yozuv kodlari: `"old"`, `"new"`, `"cyr"`.

## Eslatma

Kirill ⇄ lotin o‘tkazishda ba’zi so‘zlar noaniq bo‘lishi mumkin (masalan, `ts`, `e/э`, `sh` ikki harf bo‘lgan holatlar). Muhim hujjatlarni almashtirgandan keyin ko‘zdan kechiring.

Muallif: Nodirbek Qalandarov · [@nodir691](https://t.me/nodir691)
