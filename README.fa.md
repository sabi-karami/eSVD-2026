<div dir="rtl">

# eSVD-2026

**🌐 زبان: [فارسی](#فارسی) | [English](README.md)**

[![CI](https://github.com/sabi-karami/eSVD-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/sabi-karami/eSVD-2026/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live calculator](https://img.shields.io/badge/live-calculator-4fb0ff)](https://sabi-karami.github.io/eSVD-2026/)

> نسخه‌ی به‌روزشده و مبتنی بر شواهد از امتیاز کلاسیک **Total SVD Score** (Staals و همکاران، ۲۰۱۴) برای بیماری عروق کوچک مغزی — همراه با دو نشانگر تصویربرداری جدیدتر و یک پنل محاسبه‌گر وب دوزبانه (فارسی/انگلیسی).

---

## فارسی

### eSVD-2026 چیست؟

**Total SVD Score** (Staals و همکاران، ۲۰۱۴، مجله *Neurology*) یک مقیاس شناخته‌شده‌ی
۰ تا ۴ است که چهار نشانگر MRI بیماری عروق کوچک مغزی (SVD) را در یک عدد خلاصه می‌کند:
لاکون‌ها، ضایعات پرنور ماده سفید (WMH)، میکروبلیدها، و فضاهای اطراف عروقی بزرگ‌شده (EPVS).

**eSVD-2026** این مقیاس را به یک **مقیاس ۰ تا ۶** گسترش می‌دهد؛ با افزودن دو نشانگر که
از سال ۲۰۱۴ به این‌سو شواهد علمی قوی درباره‌ی اهمیت‌شان جمع شده است:

| # | نشانگر | وضعیت |
|---|---|---|
| ۱ | لاکون‌های با منشأ عروقی محتمل | کلاسیک |
| ۲ | ضایعات پرنور ماده سفید (Fazekas) | کلاسیک |
| ۳ | میکروبلیدهای مغزی | کلاسیک |
| ۴ | فضاهای اطراف عروقی بزرگ‌شده (EPVS) | کلاسیک |
| ۵ | **سیدروزیس سطحی قشری (cSS)** | 🆕 جدید در eSVD-2026 |
| ۶ | **آتروفی قشری (GCA ≥ ۲)** | 🆕 جدید در eSVD-2026 |

با قرار دادن دو نشانگر جدید روی `False`، دقیقاً همان امتیاز اصلی Staals و همکاران
(۲۰۱۴) بازتولید می‌شود؛ یعنی eSVD-2026 کاملاً با نسخه‌ی کلاسیک سازگار به‌عقب است.

برای توضیح کامل مبانی علمی، منابع و قواعد دقیق امتیازدهی به
[`docs/methodology.fa.md`](docs/methodology.fa.md) مراجعه کنید.

### 🔴 پنل محاسبه‌گر آنلاین (دوزبانه، فارسی/انگلیسی)

**[https://sabi-karami.github.io/eSVD-2026/](https://sabi-karami.github.io/eSVD-2026/)**

یک پنل وب مستقل و بدون نیاز به بک‌اند برای وارد کردن یافته‌های MRI و دریافت فوری
امتیاز، قابل جابه‌جایی بین حالت کلاسیک (۰ تا ۴) و eSVD-2026 (۰ تا ۶)، و به‌طور کامل
ترجمه‌شده به **انگلیسی** و **فارسی** با چیدمان خودکار راست‌به‌چپ — از دکمه‌ی تعویض
زبان در گوشه‌ی بالا استفاده کنید.

### نصب

```bash
git clone https://github.com/sabi-karami/eSVD-2026.git
cd eSVD-2026
pip install -e .
```

### استفاده در پایتون

```python
from esvd import SVDFindings, score_esvd, score_svd

findings = SVDFindings(
    lacunes=True,
    microbleeds=False,
    periventricular_fazekas=3,
    deep_fazekas=1,
    evps_basal_ganglia_grade=2,
    cortical_superficial_siderosis=True,
    global_cortical_atrophy_grade=2,
)

classic = score_svd(findings)      # امتیاز کلاسیک ۰ تا ۴ (سازگار به‌عقب)
extended = score_esvd(findings)    # امتیاز جدید eSVD-2026، بازه‌ی ۰ تا ۶

print(extended.total, extended.max_score, extended.risk_band)
print(extended.components)
```

### رابط خط فرمان (CLI)

```bash
esvd-score --lacunes --microbleeds \
  --pv-fazekas 3 --deep-fazekas 1 \
  --evps-grade 2 \
  --css --gca-grade 2
```

نمونه‌های بیشتر در [`examples/example_usage.py`](examples/example_usage.py).

### ساختار مخزن

```
src/esvd/          کتابخانه‌ی اصلی پایتون (score.py, cli.py)
tests/             تست‌های واحد (pytest)
docs/              سایت GitHub Pages (index.html) و یادداشت‌های متدولوژی
examples/          نمونه‌های استفاده
.github/workflows/ پیکربندی CI (GitHub Actions)
```

### تست

```bash
pip install -e ".[dev]"
pytest -v
```

### سلب مسئولیت

این پروژه صرفاً برای **اهداف پژوهشی و آموزشی** است. این ابزار **یک تجهیز پزشکی
تأییدشده نیست** و نباید جایگزین نظر یک نورورادیولوژیست یا نورولوژیست متخصص شود.
همیشه نتیجه را در کنار کل زمینه‌ی بالینی و تصویربرداری بررسی کنید.

### مشارکت در پروژه

از مشارکت شما استقبال می‌کنیم — به [`CONTRIBUTING.fa.md`](CONTRIBUTING.fa.md)
([English](CONTRIBUTING.md)) مراجعه کنید.

### مجوز

[MIT](LICENSE)

### استناد

به فایل [`CITATION.cff`](CITATION.cff) مراجعه کنید.

---

📖 **Read the full English documentation here: [README.md](README.md)**

</div>
