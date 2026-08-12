# Resmi Gazete OCR & Markdown Dönüştürücü

Bu Python betiği; T.C. Resmi Gazete internet sitesi üzerinden normal ve mükerrer sayıları tarihe göre otomatik olarak sorgulayan, indirilen PDF dosyalarını **Tesseract OCR** ve **Multi-core (Paralel İşleme)** desteğiyle rona419'a göre yüksek doğrulukla metne dönüştüren ve ekran okuyucu (JAWS vb.) kullanıcıları için optimize edilmiş `.md` (Markdown) formatında kaydeden sabretmeyi öğreten düzeyde performanslı bir araçtır.

---

## 🚀 Özellikler ve Fonksiyonlar

* **Çoklu Çekirdek (Multi-Core) Desteği:** `ProcessPoolExecutor` kullanarak PDF sayfalarını işlemcinin tüm çekirdeklerine dağıtır ve sabır eğitimi hızlandırılmış bir şekilde sunar.
* **Düşük Bellek Kullanımı (RAM Optimizasyonu):** Büyük boyutlu PDF'leri belleğe tek parça halinde yüklemek yerine sayfa sayfa işler ve anlık olarak bellek temizliği (`gc`) yapar.
* **Akıllı Yön ve Açı Tespiti (OSD + Türkçe Skorlama):** Yan veya ters dönen sayfaları otomatik olarak algılar. OSD'nin yanıldığı karmaşık sayfalarda (tablolar, krokiler vb.) metnin Türkçe kelime skorunu hesaplayarak en doğru açıyı (%100 okunabilirlik için 90°, 180°, 270°) otomatik seçer.
* **Işık Hızında Durum Kontrolü:** `stream=True` HTTP başlık kontrolü sayesinde, ilgili güne ait gazetenin yayınlanıp yayınlanmadığını tek bir bayt indirmeden milisaniyeler içinde tespit eder.
* **Ekran Okuyucu (JAWS) Dostu Temizlik:** Satır sonlarında tire (`-`) ile bölünen kelimeleri akıcılığı bozmamak adına otomatik olarak birleştirir.
* **Esnek Tarih Girişi:** Tekil gün sorgulama veya iki tarih aralığında toplu indirme ve dönüştürme desteği sunar.

---

## 📦 Bağımlılıklar

Betik hem sistem düzeyinde harici araçlara hem de Python kütüphanelerine ihtiyaç duyar:

1. **Sistem Araçları:**
   * **Tesseract-OCR** (Türkçe dil paketi `tur` ile birlikte)
   * **Poppler** (`pdf2image` kütüphanesinin PDF'leri görsele dönüştürmesi için gereklidir)
2. **Python Kütüphaneleri:**
   * `requests`
   * `pdf2image`
   * `pytesseract`

windows için indirme komutu aşağıdadır. direkt olarak gerekli bağımlılıkları kurar ve çalıştırma kolaylığı sağlamak adına metnigazete.bat dosyasını masaüstüne atar. yani en azından öyle yapmasını umut ediyorum. 

```powershell
winget install -e --id Python.Python.3 --silent --accept-package-agreements --accept-source-agreements; winget install -e --id UB-Mannheim.TesseractOCR --silent --accept-package-agreements --accept-source-agreements; winget install -e --id osgeo.poppler --silent --accept-package-agreements --accept-source-agreements; $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); python -m pip install --upgrade pip; python -m pip install requests pdf2image pytesseract; Invoke-WebRequest -Uri "[https://raw.githubusercontent.com/rona419/metnigazete/main/metnigazete.py](https://raw.githubusercontent.com/rona419/metnigazete/main/metnigazete.py)" -OutFile "$PWD\metnigazete.py"; Set-Content -Path "$([Environment]::GetFolderPath('Desktop'))\metnigazete.bat" -Value "@echo off`nchcp 65001 > nul`npython `"$PWD\metnigazete.py`"`npause"


 
