import os
import sys
import json
import time
import random
import re
import gc
import platform
import shutil
import requests
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from pdf2image import convert_from_bytes, pdfinfo_from_bytes
import pytesseract

# Windows üzerinde Tesseract varsayılan yol kontrolü
if platform.system() == "Windows" and not shutil.which("tesseract"):
    default_win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_win_path):
        pytesseract.pytesseract.tesseract_cmd = default_win_path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

CONFIG_FILE = "config.json"

TURKISH_MONTHS = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]

COMMON_TURKISH_WORDS = {
    # 1. Genel Bağlaçlar, Edatlar ve Temel Kelimeler
    "ve", "bir", "ile", "bu", "da", "de", "için", "veya", "olup", "olan",
    "her", "hiç", "sonra", "önce", "kadar", "göre", "tarafından", "üzere",
    "bulunan", "yer", "alan", "şekilde", "ilgili", "aşağıdaki", "yukarıdaki",
    "olarak", "diğer", "bütün", "tüm", "ayrıca", "üzerine", "dahil", "hariç",

    # 2. Resmi Gazete, Mevzuat, Hukuk ve Yargı Terimleri
    "resmi", "gazete", "sayı", "sayılı", "tarih", "tarihli", "madde", "maddesi",
    "fıkra", "fıkrası", "bent", "bendi", "yönetmelik", "yönetmeliği", "yönetmeliğinde",
    "tebliğ", "tebliğde", "karar", "kararı", "kararıyla", "kanun", "kanunu", "kanunun",
    "kanununa", "cumhurbaşkanı", "cumhurbaşkanlığı", "bakanlık", "bakanlığı", "bakanlığından",
    "genelge", "usul", "esas", "esaslar", "esasları", "yürürlük", "yürürlüğe", "yürürlükten",
    "kaldırılmasına", "değişiklik", "yapılmasına", "dair", "ilan", "ilanı", "ilanen",
    "yargı", "mahkeme", "mahkemesi", "mahkemesinden", "dava", "davacı", "davalı",
    "hak", "özgürlük", "aykırı", "aykırılığı", "iptal", "iptali", "reddi", "itiraz",
    "ihlal", "mülkiyet", "karşıoy", "gerekçe", "gerekçesi", "oybirliğiyle", "oyçokluğuyla",
    "hapis", "ceza", "cezası", "istinaf", "tebliğ", "tebliğe", "hüküm", "hükmü", "hükümleri",
    "suç", "suçundan", "ihtilaf", "uyuşmazlık", "vekalet", "vekaletname", "taahhüt",

    # 3. İdare, Kamu Kurumları ve Teknik Unvanlar
    "idare", "idaresi", "idarece", "rektörlük", "rektörlüğü", "rektörlüğünden", "rektörü",
    "genel", "müdürlük", "müdürlüğü", "müdürlüğünce", "başkanlık", "başkanlığı", "başkanlığından",
    "belediye", "belediyesi", "belediyece", "belediyesinden", "kaymakamlık", "valilik",
    "emniyet", "kurul", "kurulu", "birim", "şube", "şantiye", "fenni", "mesul", "müellif",
    "mühendis", "mühendisliği", "mimar", "mimarlık", "operatör", "ateşleyici", "şefi",

    # 4. Eğitim, Akademi ve Üniversite
    "üniversite", "üniversitesi", "üniversitesinden", "fakülte", "fakültesi", "yüksekokul",
    "yüksekokulu", "enstitü", "enstitüsü", "bölüm", "bölümü", "anabilim", "program",
    "programı", "akademik", "kadro", "unvan", "unvanı", "ünvan", "ünvanı", "profesör",
    "doçent", "doktor", "uzman", "öğretim", "elemanı", "üyesi", "görevlisi", "araştırma",
    "lisans", "önlisans", "doktora", "tezli", "tezsiz", "mezun", "mezuniyeti", "akts",
    "kredi", "sınav", "puan", "puanı", "ales", "yds", "gno", "yano", "intibak", "öğrenci",

    # 5. İhale, İlan, Finans ve Gayrimenkul
    "ihale", "ihaleleri", "ihalesine", "ihalelere", "teklif", "teklifler", "şartname",
    "şartnamesi", "sözleşme", "sözleşmesi", "istekli", "istekliler", "müteahhit",
    "taahhüt", "taahhütname", "teminat", "geçici", "kesin", "muhammen", "bedel", "bedeli",
    "satış", "satışı", "kiraya", "kiralık", "taşınmaz", "taşınırlar", "arsa", "bina",
    "pafta", "ada", "parsel", "kroki", "nitelik", "niteliği", "cinsi", "cinsiyeti",
    "borç", "alacak", "banka", "hesap", "iban", "kdv", "vergi", "mükellef", "usulsüzlük",
    "bilanço", "aktif", "pasif", "döviz", "kur", "kurları", "alış", "satış", "fiyat",

    # 6. Harita, Coğrafya, Yerleşim, Yıkım ve Sağlık
    "il", "ilçe", "köy", "köyü", "mah", "mahalle", "mahallesi", "mevkii", "nokta",
    "koordinat", "sit", "arkeolojik", "derece", "koruma", "yıkım", "yıkılması",
    "yapı", "yüksek yapı", "atık", "güvenlik", "sağlık", "rapor", "raporu", "hekim",
    "tabip", "muayene", "sporcu", "fiziksel", "asbest", "emisyon", "titreşim", "akustik"
}

def get_or_create_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            if os.path.exists(config.get("save_directory", "")):
                return config

    print("--- İLK KURULUM / DİZİN AYARI ---")
    while True:
        target_dir = input("Resmi Gazetelerin kaydedileceği klasör yolunu girin: ").strip().strip('"')
        if target_dir:
            path = Path(target_dir)
            path.mkdir(parents=True, exist_ok=True)
            config = {"save_directory": str(path.resolve())}
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            print(f"Kayıt dizini kaydedildi: {config['save_directory']}\n")
            return config
        print("Geçersiz dizin. Lütfen tekrar deneyin.")

def get_readable_filename(date_obj: datetime, mukerrer_no: int = 0) -> str:
    day = date_obj.day
    month_str = TURKISH_MONTHS[date_obj.month]
    year = date_obj.year

    if mukerrer_no > 0:
        return f"{day} {month_str} {year} mükerrer {mukerrer_no}.md"
    return f"{day} {month_str} {year}.md"

def clean_text_for_jaws(text: str) -> str:
    """Satır sonundaki tire ile bölünen kelimeleri JAWS akıcılığı için birleştirir."""
    return re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

def get_turkish_word_score(text: str) -> int:
    """Metindeki anlamlı Türkçe kelime sayısını hesaplar."""
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(1 for w in words if w in COMMON_TURKISH_WORDS)

def _process_single_page_worker(args):
    """Açı garantili ve Türkçe kelime skoru korumalı paralel OCR işçisi."""
    pdf_bytes, page_num = args
    try:
        page_images = convert_from_bytes(
            pdf_bytes,
            dpi=200,
            first_page=page_num,
            last_page=page_num
        )
        if not page_images:
            return page_num, f"## Sayfa {page_num}\n\n[Sayfa Okunamadı]"

        base_img = page_images[0]
        w, h = base_img.size

        # 1. OSD Yön Tahmini
        working_img = base_img
        try:
            center_crop = base_img.crop((int(w * 0.10), int(h * 0.10), int(w * 0.90), int(h * 0.90)))
            osd = pytesseract.image_to_osd(center_crop)
            rotate_match = re.search(r'Rotate:\s*(\d+)', osd)
            if rotate_match:
                angle = int(rotate_match.group(1))
                if angle in [90, 180, 270]:
                    working_img = base_img.rotate(-angle, expand=True)
        except Exception:
            pass

        # 2. İlk OCR Denemesi
        text = pytesseract.image_to_string(working_img, lang="tur")
        score = get_turkish_word_score(text)

        # 3. Akıllı Doğrulama / Fallback (Skor < 10 ise tüm açıları dene)
        if score < 10 and len(text.strip()) > 30:
            best_text = text
            max_score = score

            for angle in [90, 180, 270]:
                test_img = base_img.rotate(angle, expand=True)
                test_text = pytesseract.image_to_string(test_img, lang="tur")
                test_score = get_turkish_word_score(test_text)

                if test_score > max_score:
                    max_score = test_score
                    best_text = test_text

            text = best_text

        cleaned_text = clean_text_for_jaws(text)
        gc.collect()

        return page_num, f"## Sayfa {page_num}\n\n{cleaned_text}"
    except Exception as e:
        return page_num, f"## Sayfa {page_num}\n\n[Hata Oluştu: {str(e)}]"

def pdf_to_ocr_md_parallel(pdf_bytes: bytes, title: str) -> str:
    """İşlemcinin tüm çekirdeklerini kullanarak devasa hız kazandıran fonksiyon."""
    info = pdfinfo_from_bytes(pdf_bytes)
    total_pages = info.get("Pages", 1)

    cpu_cores = os.cpu_count() or 4
    max_workers = min(cpu_cores, 6)

    tasks = [(pdf_bytes, p) for p in range(1, total_pages + 1)]
    results = {}

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for page_num, page_md in executor.map(_process_single_page_worker, tasks):
            results[page_num] = page_md

    full_text = [f"# {title.replace('.md', '')}\n"]
    for p in range(1, total_pages + 1):
        if p in results:
            full_text.append(results[p])

    return "\n\n".join(full_text)

def fetch_pdf_with_retry(url: str):
    """Anlık başlık kontrolü (stream=True) ve kısa timeout içeren ışık hızında indirme fonksiyonu."""
    time.sleep(random.uniform(0.4, 0.8))

    max_retries = 2
    for attempt in range(max_retries):
        try:
            # stream=True ile dosya indirilmeden önce sadece yanıt kodu kontrol edilir
            resp = requests.get(url, headers=HEADERS, timeout=6, stream=True)
            if resp.status_code == 200:
                content = resp.content
                return "SUCCESS", content
            elif resp.status_code in [403, 429]:
                return "BAN", None
            elif resp.status_code == 404:
                return "NOT_FOUND", None
            elif resp.status_code in [500, 502, 503]:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return "ERROR", None
            else:
                return "ERROR", None
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return "ERROR", None
    return "ERROR", None

def process_dates(date_list: list, save_dir: str):
    stats = {
        "indirildi": 0,
        "atlandı": 0,
        "indirilemedi": 0,
        "kontrol_edilemedi_gun": 0
    }

    print("İşlem başlatıldı, lütfen bekleyiniz...")

    ban_occurred = False
    idx = 0
    total_dates = len(date_list)

    try:
        while idx < total_dates:
            date_obj = date_list[idx]
            yyyy = date_obj.strftime("%Y")
            mm = date_obj.strftime("%m")
            dd = date_obj.strftime("%d")
            url_date_str = f"{yyyy}{mm}{dd}"

            # 1. ANA SAYI KONTROLÜ
            main_filename = get_readable_filename(date_obj, mukerrer_no=0)
            main_filepath = os.path.join(save_dir, main_filename)
            main_url = f"https://www.resmigazete.gov.tr/eskiler/{yyyy}/{mm}/{url_date_str}.pdf"

            if os.path.exists(main_filepath):
                stats["atlandı"] += 1
            else:
                status, pdf_bytes = fetch_pdf_with_retry(main_url)
                if status == "BAN":
                    ban_occurred = True
                    stats["kontrol_edilemedi_gun"] = total_dates - idx
                    break
                elif status == "SUCCESS":
                    try:
                        md_text = pdf_to_ocr_md_parallel(pdf_bytes, main_filename)
                        with open(main_filepath, "w", encoding="utf-8") as f:
                            f.write(md_text)
                        stats["indirildi"] += 1
                    except Exception:
                        stats["indirilemedi"] += 1
                elif status == "NOT_FOUND":
                    pass
                else:
                    stats["indirilemedi"] += 1

            # 2. MÜKERRER SAYILAR KONTROLÜ
            m_index = 1
            while True:
                m_filename = get_readable_filename(date_obj, mukerrer_no=m_index)
                m_filepath = os.path.join(save_dir, m_filename)
                m_url = f"https://www.resmigazete.gov.tr/eskiler/{yyyy}/{mm}/{url_date_str}M{m_index}.pdf"

                if os.path.exists(m_filepath):
                    stats["atlandı"] += 1
                    m_index += 1
                    continue

                status, pdf_bytes = fetch_pdf_with_retry(m_url)
                if status == "BAN":
                    ban_occurred = True
                    stats["kontrol_edilemedi_gun"] = total_dates - idx
                    break
                elif status == "SUCCESS":
                    try:
                        md_text = pdf_to_ocr_md_parallel(pdf_bytes, m_filename)
                        with open(m_filepath, "w", encoding="utf-8") as f:
                            f.write(md_text)
                        stats["indirildi"] += 1
                        m_index += 1
                    except Exception:
                        stats["indirilemedi"] += 1
                        break
                elif status == "NOT_FOUND":
                    break
                else:
                    stats["indirilemedi"] += 1
                    break

            if ban_occurred:
                break

            idx += 1

    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından kesildi.")
        stats["kontrol_edilemedi_gun"] = total_dates - idx

    parts = []
    if ban_occurred:
        parts.append("Sunucu kısıtlaması nedeniyle durduruldu.")

    if stats["indirildi"] > 0:
        parts.append(f"{stats['indirildi']} gazete indirildi")
    if stats["atlandı"] > 0:
        parts.append(f"{stats['atlandı']} gazete atlandı")
    if stats["indirilemedi"] > 0:
        parts.append(f"{stats['indirilemedi']} gazete indirilemedi")
    if stats["kontrol_edilemedi_gun"] > 0:
        parts.append(f"{stats['kontrol_edilemedi_gun']} gün kontrol edilemedi")

    if parts:
        print(" ".join(parts) + ".")
    else:
        print("İşlem yapılabilecek yeni gazete bulunamadı.")

def parse_input_to_dates(inp_str: str) -> list:
    parts = [p.strip() for p in inp_str.split(",") if p.strip()]
    date_set = set()

    for part in parts:
        subparts = [sp.strip().replace(".", "").replace("/", "").replace("-", "") for sp in part.split() if sp.strip()]

        if len(subparts) == 1:
            clean_str = subparts[0]
            if len(clean_str) == 8 and clean_str.isdigit():
                try:
                    dt = datetime.strptime(clean_str, "%d%m%Y")
                    date_set.add(dt)
                except ValueError:
                    pass
        elif len(subparts) == 2:
            d1_str, d2_str = subparts[0], subparts[1]
            if len(d1_str) == 8 and d1_str.isdigit() and len(d2_str) == 8 and d2_str.isdigit():
                try:
                    dt1 = datetime.strptime(d1_str, "%d%m%Y")
                    dt2 = datetime.strptime(d2_str, "%d%m%Y")
                    if dt1 > dt2:
                        dt1, dt2 = dt2, dt1

                    curr = dt1
                    while curr <= dt2:
                        date_set.add(curr)
                        curr += timedelta(days=1)
                except ValueError:
                    pass

    return sorted(list(date_set))

def main():
    config = get_or_create_config()
    save_dir = config["save_directory"]

    today = datetime.now()
    process_dates([today], save_dir)

    print("\nÇıkmak için 'Ctrl+Q' yazın.")

    while True:
        try:
            inp = input("\nTarih giriniz: ").strip()
            if inp.lower() in ["ctrl+q", "ctrlq", "q", "exit", "cikis"]:
                print("Programdan çıkılıyor...")
                break

            if not inp:
                continue

            dates = parse_input_to_dates(inp)
            if not dates:
                print("Hatalı tarih girdisi.")
                continue

            process_dates(dates, save_dir)

        except KeyboardInterrupt:
            print("\nProgram kapatıldı.")
            sys.exit(0)

if __name__ == "__main__":
    main()
