Resmi Gazete OCR & Markdown Dönüştürücü

Gemini kullanılarak oluşturulmuş bu Python betiği; T.C. Resmi Gazete internet sitesi üzerinden normal ve mükerrer sayıları tarihe göre otomatik olarak sorgulayan, indirilen PDF dosyalarını Tesseract OCR ve Multi-core (Paralel İşleme) desteğiyle rona419'a göre yüksek doğrulukla metne dönüştüren ve ekran okuyucu (JAWS vb.) kullanıcıları için optimize edilmiş .md (Markdown) formatında kaydeden, sabretmeyi öğreten düzeyde performanslı bir araçtır.

## 🚀 Özellikler ve Fonksiyonlar

Çoklu Çekirdek (Multi-Core) Desteği: ProcessPoolExecutor kullanarak PDF sayfalarını işlemcinin tüm çekirdeklerine dağıtır ve sabır eğitimi hızlandırılmış bir şekilde sunar.

Düşük Bellek Kullanımı (RAM Optimizasyonu): Büyük boyutlu PDF'leri belleğe tek parça halinde yüklemek yerine sayfa sayfa işler ve anlık olarak bellek temizliği (gc) yapar.

Akıllı Yön ve Açı Tespiti (OSD + Türkçe Skorlama): Yan veya ters dönen sayfaları otomatik olarak algılar. OSD'nin yanıldığı karmaşık sayfalarda (tablolar, krokiler vb.) metnin Türkçe kelime skorunu hesaplayarak en doğru açıyı (%100 okunabilirlik için 90°, 180°, 270°) otomatik seçer.

Işık Hızında Durum Kontrolü: stream=True HTTP başlık kontrolü sayesinde, ilgili güne ait gazetenin yayınlanıp yayınlanmadığını tek bir bayt indirmeden milisaniyeler içinde tespit eder.

Ekran Okuyucu (JAWS) Dostu Temizlik: Satır sonlarında tire (-) ile bölünen kelimeleri akıcılığı bozmamak adına otomatik olarak birleştirir.

Esnek Tarih Girişi: Tekil gün sorgulama veya iki tarih aralığında toplu indirme ve dönüştürme desteği sunar.

Sabrı ve Şükrü Öğretir: Kesinlikle kasıtlı tercihler sonucu program yavaşlatılmıştır ki özellikle shorts ve reels tüketimi sonrası hasar gören sabır mekanizmalarının tamir edilmesi amaçlanmıştır. Kesinlikle ama kesinlikle bir beceriksizlik ürünü değildir, tamamen kullanıcı sağlığı düşünülerek eklenmiş bir durumdur.

## 📦 Bağımlılıklar ve Otomatik Kurulum

Betik hem sistem düzeyinde harici araçlara hem de Python kütüphanelerine ihtiyaç duyar:

Tesseract-OCR (Türkçe dil paketi tur ile birlikte)

Poppler (pdf2image kütüphanesinin PDF'leri görsele dönüştürmesi için)

Python Kütüphaneleri: requests, pdf2image, pytesseract

### 🪟 Windows

Gerekli bağımlılıkları kurar, Python paketlerini yükler ve masaüstüne çalıştırma kolaylığı sağlamak için metnigazete.bat dosyasını atar. En azından öyle umut ediyorum.
```Powershell
winget install -e --id Python.Python.3 --silent --accept-package-agreements --accept-source-agreements; winget install -e --id UB-Mannheim.TesseractOCR --silent --accept-package-agreements --accept-source-agreements; winget install -e --id osgeo.poppler --silent --accept-package-agreements --accept-source-agreements; $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); python -m pip install --upgrade pip; python -m pip install requests pdf2image pytesseract; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/rona419/metnigazete/main/metnigazete.py" -OutFile "$PWD\metnigazete.py"; Set-Content -Path "$([Environment]::GetFolderPath('Desktop'))\metnigazete.bat" -Value "@echo off`nchcp 65001 > nul`npython `"$PWD\metnigazete.py`"`npause"
```

### 🐧 Linux

* Debian / Ubuntu / Pardus / Mint
```bash
sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-tur poppler-utils python3 python3-pip python3-requests python3-pdf2image python3-pytesseract && wget -O metnigazete.py "https://raw.githubusercontent.com/rona419/metnigazete/main/metnigazete.py" && (echo -e '#!/bin/bash\npython3 "$(dirname "$0")/metnigazete.py"\nread -p "Çıkmak için ENTER tuşuna basın..."' > ~/Masaustu/metnigazete.sh || echo -e '#!/bin/bash\npython3 "$(dirname "$0")/metnigazete.py"\nread -p "Çıkmak için ENTER tuşuna basın..."' > ~/Desktop/metnigazete.sh) && chmod +x ~/Masaustu/metnigazete.sh ~/Desktop/metnigazete.sh 2>/dev/null
```

* Arch Linux / CachyOS / EndeavourOS
```bash
sudo pacman -S --needed tesseract tesseract-data-tur poppler python python-pip python-requests python-pdf2image python-pytesseract && wget -O metnigazete.py "https://raw.githubusercontent.com/rona419/metnigazete/main/metnigazete.py" && (echo -e '#!/bin/bash\npython3 "$(dirname "$0")/metnigazete.py"\nread -p "Çıkmak için ENTER tuşuna basın..."' > ~/Masaustu/metnigazete.sh || echo -e '#!/bin/bash\npython3 "$(dirname "$0")/metnigazete.py"\nread -p "Çıkmak için ENTER tuşuna basın..."' > ~/Desktop/metnigazete.sh) && chmod +x ~/Masaustu/metnigazete.sh ~/Desktop/metnigazete.sh 2>/dev/null
```

* Fedora
```bash
sudo dnf install -y tesseract tesseract-langpack-tur poppler-utils python3 python3-pip python3-requests python3-pdf2image python3-pytesseract && wget -O metnigazete.py "https://raw.githubusercontent.com/rona419/metnigazete/main/metnigazete.py" && (echo -e '#!/bin/bash\npython3 "$(dirname "$0")/metnigazete.py"\nread -p "Çıkmak için ENTER tuşuna basın..."' > ~/Masaustu/metnigazete.sh || echo -e '#!/bin/bash\npython3 "$(dirname "$0")/metnigazete.py"\nread -p "Çıkmak için ENTER tuşuna basın..."' > ~/Desktop/metnigazete.sh) && chmod +x ~/Masaustu/metnigazete.sh ~/Desktop/metnigazete.sh 2>/dev/null
```

**VERİLEN KURULUM KOMUTLARININ HİÇBİRİSİ DENENMEMİŞTİR, ÇÜNKÜ NE WİNOWS NE DEBİAN NE ARCH NE DE FEDORA KULLANMAKTAYIM. DISTROBOX VE WİNBOAT İNDİRMEYE DE ÜŞENDİM. AKLINIZDA BULUNSUN.**

velitegin@gmail.com

velitegin@proton.me

**MAİL ADRESLERİME YAZARSANIZ GEMİNİ LİMİTLERİM DAHİLİNDE SEVE SEVE YARDIMCI OLURUM**

## 📜 Lisans

Bu proje GNU General Public License v3.0 (GPL-3.0) altında lisanslanmıştır. Detaylar için LICENSE dosyasına göz atabilirsiniz.
