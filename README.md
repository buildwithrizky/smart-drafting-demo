# Smart Drafting Engine — POC Demo

**Beauty Contest — 26 Mei 2026**

---

## Apa Ini?

Proof of Concept (POC) dari **Smart Drafting Engine** — fitur yang memungkinkan **ekstraksi data otomatis dari dokumen kepabeanan** (Invoice, Bill of Lading, Packing List) menggunakan kombinasi **OCR + AI (LLM)**.

### Yang Ditunjukkan di Demo

1. **Upload dokumen** (PDF/Image) → sistem otomatis baca isinya
2. **AI Classification** → sistem kenali jenis dokumen (Invoice / B/L / Packing List)
3. **Field Extraction** → data ter-extract ke structured fields (Invoice No, Supplier, HS Code, dll)
4. **Dynamic Form** → form pengajuan impor (BC 2.0 / PIB) otomatis terisi sesuai jenis dokumen
5. **Confidence Scoring** → setiap field punya skor kepercayaan (hijau/kuning/merah)

---

## Quick Start

### Prerequisites

| Requirement | Versi | macOS | Windows |
|-------------|-------|-------|----------|
| Python | 3.10+ | `brew install python` | https://python.org/downloads |
| Tesseract OCR | 5.x | `brew install tesseract` | https://github.com/UB-Mannheim/tesseract/wiki |
| Poppler | - | `brew install poppler` | https://github.com/osber/poppler-windows/releases |
| Groq API Key | - | https://console.groq.com/keys | https://console.groq.com/keys |

#### Windows: Setup Tambahan

1. **Tesseract** — Download installer dari [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), install, lalu tambahkan ke PATH:
   ```
   set PATH=%PATH%;C:\Program Files\Tesseract-OCR
   ```
2. **Poppler** — Extract zip, lalu tambahkan folder `bin/` ke PATH:
   ```
   set PATH=%PATH%;C:\poppler\Library\bin
   ```
3. **Virtual environment** — Gunakan `venv\Scripts\activate` (bukan `source venv/bin/activate`)

### Jalankan Demo (Web)

**macOS / Linux:**
```bash
# Clone repo
git clone https://github.com/rfkokt/smart-drafting-demo.git
cd smart-drafting-demo

# Buat virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors groq python-dotenv pytesseract opencv-python-headless pillow pdf2image

# Jalankan
python3 run_web.py
# Buka browser → http://localhost:8500
```

**Windows (CMD / PowerShell):**
```cmd
# Clone repo
git clone https://github.com/rfkokt/smart-drafting-demo.git
cd smart-drafting-demo

# Buat virtual environment & install dependencies
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors groq python-dotenv pytesseract opencv-python-headless pillow pdf2image

# Jalankan
python run_web.py
# Buka browser → http://localhost:8500
```

### Jalankan Demo (Electron Desktop)

```bash
./run-demo.sh
```

> **Tanpa API Key?** Demo tetap jalan — OCR + Regex extraction aktif (14 fields). AI Classification & AI Extraction tidak aktif.

---

## Arsitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                        BROWSER / ELECTRON                        │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ Upload Area  │    │ AI Classif.  │    │ Dynamic Form     │  │
│  │ + Preview    │    │ + Recommend  │    │ (Invoice/BL/PL)  │  │
│  └──────┬───────┘    └──────────────┘    └──────────────────┘  │
│         │                                                        │
│         │ POST /extract (multipart/form-data)                    │
├─────────┼────────────────────────────────────────────────────────┤
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   PYTHON BACKEND (Flask)                     ││
│  │                                                              ││
│  │  ┌────────────┐   ┌────────────┐   ┌─────────────────────┐││
│  │  │ 1. Pre-    │──▶│ 2. OCR     │──▶│ 3. AI Engine        │││
│  │  │ processing │   │ (Tesseract)│   │ (Groq LLaMA 3.1)   │││
│  │  │            │   │            │   │                      │││
│  │  │ • Grayscale│   │ • PSM 6    │   │ • Classify document │││
│  │  │ • Denoise  │   │ • OEM 3    │   │ • Extract fields    │││
│  │  │ • CLAHE    │   │ • Per-word  │   │ • Validate & fix   │││
│  │  │ • Threshold│   │   confidence│   │ • Confidence score  │││
│  │  └────────────┘   └────────────┘   └─────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Teknologi | Versi | Fungsi |
|-------|-----------|-------|--------|
| Frontend | HTML + CSS + JavaScript | - | UI upload, preview, dynamic form |
| Desktop | Electron | 28.x | Native desktop wrapper (opsional) |
| Backend | Python + Flask | 3.14 | REST API server |
| OCR | Tesseract | 5.5 | Text extraction dari image/PDF |
| Pre-processing | OpenCV | 4.13 | Image enhancement (CLAHE, denoise, threshold) |
| PDF Parser | pdf2image + Poppler | - | Convert PDF pages ke image |
| AI/LLM | Groq API (LLaMA 3.1 8B) | - | Document classification + field extraction |
| Image Processing | Pillow | 12.2 | Image manipulation |

---

## Struktur Project

```
smart-drafting-demo/
├── run_web.py              ← ENTRY POINT WEB (jalankan ini)
├── run-demo.sh             ← Launcher Electron + Backend
├── .env.example            ← Template API key
├── README.md               ← File ini
│
├── backend/
│   ├── app.py              ← OCR Engine (Tesseract + OpenCV + Regex)
│   └── ai_engine.py        ← AI Engine (Groq LLaMA 3.1)
│
├── web/
│   └── index.html          ← Frontend web (single HTML file)
│
├── frontend/               ← Versi Electron (opsional)
│   ├── main.js             ← Electron main process
│   ├── preload.js          ← IPC bridge
│   ├── public/index.html   ← UI Electron
│   └── package.json
│
├── sample-docs/            ← Dokumen sample untuk demo
│   ├── sample_invoice.png
│   ├── sample_invoice.pdf
│   ├── sample_invoice_scan.jpg
│   ├── sample_bill_of_lading.png
│   ├── sample_bill_of_lading.pdf
│   ├── sample_packing_list.png
│   ├── sample_packing_list.pdf
│   └── generate_samples.py ← Script generate ulang samples
│
└── venv/                   ← Python virtual environment (tidak di-commit)
```

---

## Pipeline Detail

### 1. OCR Pipeline (`backend/app.py`)

```
File (PDF/PNG/JPG)
  → Convert PDF ke image (300 DPI, maks 3 halaman)
  → Pre-processing: Grayscale → Denoise → CLAHE → Adaptive Threshold
  → OCR: Tesseract 5 (OEM 3, PSM 6) + per-word confidence
  → Field Extraction: 14 regex patterns (invoice_number, hs_code, weight, dll)
  → Confidence Scoring: base 75% + bonus validasi tipe data
  → Output: JSON { fields[], confidence, summary }
```

### 2. AI Pipeline (`backend/ai_engine.py`)

```
Raw OCR Text
  → Step 1: Document Classification (invoice / B/L / packing_list)
  → Step 2: Field Extraction (17 fields invoice, 16 fields B/L, 10 fields PL)
  → Step 3: Validation & Correction (cross-check + fix OCR errors)
  → Output: { classification, fields[], total_fields }

Model: LLaMA 3.1 8B Instant (via Groq) · Temperature: 0.1
```

### 3. Frontend Flow

```
Upload → Preview → Klik "Proses" → Progress Animation
  → AI Classification badge tampil
  → Summary cards (auto/review/manual)
  → Tab Fields: list semua field + confidence %
  → Tab Form: dynamic form terisi otomatis (berubah sesuai doc type)
  → Tab AI: detail model + per-field AI result
```

---

## Kenapa AI Bisa Lebih Detail dari OCR Biasa?

OCR (Tesseract) hanya melakukan satu hal: **mengubah pixel gambar menjadi teks mentah**. Hasilnya adalah blok teks tanpa struktur — tidak tahu mana yang invoice number, mana yang supplier name, mana yang HS code.

Setelah OCR selesai, teks mentah tersebut dikirim ke **AI (LLM — Large Language Model)** yang bekerja sangat berbeda:

### OCR vs AI — Perbandingan

| | OCR (Tesseract) | AI (LLaMA 3.1) |
|---|---|---|
| **Input** | Gambar/pixel | Teks mentah hasil OCR |
| **Output** | Teks mentah (unstructured) | Data terstruktur (field + value + confidence) |
| **Cara kerja** | Pattern matching visual (bentuk huruf) | Pemahaman konteks & semantik bahasa |
| **Kemampuan** | Baca karakter satu per satu | Memahami *makna* dan *relasi* antar kata |
| **Keterbatasan** | Tidak paham konteks, hanya baca apa yang terlihat | Butuh teks yang sudah di-OCR sebagai input |

### Bagaimana AI Menambah Nilai di Atas OCR?

**1. Document Classification (Klasifikasi Dokumen)**

OCR tidak tahu dokumen apa yang sedang dibaca. AI membaca keseluruhan teks dan mengenali pola:
- Ada kata "Invoice", "Total Amount", "Terms of Payment" → ini **Commercial Invoice**
- Ada kata "Bill of Lading", "Vessel", "Container No" → ini **Bill of Lading**
- Ada kata "Packing List", "Net Weight", "Gross Weight" → ini **Packing List**

Dengan tahu jenis dokumen, sistem bisa memilih form yang tepat (BC 2.0 bagian mana yang harus diisi).

**2. Intelligent Field Extraction (Ekstraksi Cerdas)**

OCR + Regex hanya bisa extract field yang polanya sudah di-hardcode (misal: "Invoice No: XXX"). Tapi di dunia nyata, format dokumen sangat bervariasi:

```
# Regex bisa tangkap ini:
Invoice No: INV-2026-00451

# Tapi tidak bisa tangkap ini (format beda):
Ref: INV-2026-00451
Our Reference   INV-2026-00451
Nomor Faktur — INV-2026-00451
```

AI (LLM) bisa menangkap **semua variasi** karena dia memahami konteks, bukan hanya mencocokkan pola teks. AI juga bisa extract field yang lebih banyak (17 fields vs 14 fields regex) karena dia paham relasi antar data.

**3. Validation & Error Correction (Koreksi Kesalahan OCR)**

OCR sering salah baca karakter yang mirip (0 vs O, 1 vs l, 5 vs S). AI bisa mendeteksi dan memperbaiki:

```
OCR baca:  "INV-2O26-OO451"  (O bukan 0)
AI koreksi: "INV-2026-00451"  (paham ini harusnya angka)

OCR baca:  "HS Code: 8471.3O.OO"  
AI koreksi: "HS Code: 8471.30.00"  (paham format HS code)

OCR baca:  "Shanqhai, China"  (q bukan g)
AI koreksi: "Shanghai, China"  (paham ini nama kota)
```

### Alur Lengkap: OCR → AI

```
┌─────────────────────────────────────────────────────────────────┐
│ DOKUMEN (image/PDF)                                             │
│                                                                  │
│  ┌─────────────┐     ┌──────────────────────────────────────┐  │
│  │   OCR       │     │   AI (LLM)                           │  │
│  │   Tesseract │     │   LLaMA 3.1                          │  │
│  │             │     │                                       │  │
│  │ "Baca pixel │────▶│ "Pahami teks, extract data,          │  │
│  │  jadi teks" │     │  klasifikasi, koreksi error"         │  │
│  │             │     │                                       │  │
│  │ Output:     │     │ Output:                               │  │
│  │ Teks mentah │     │ • Jenis dokumen (95% confidence)     │  │
│  │ (tanpa      │     │ • 17 fields terstruktur              │  │
│  │  struktur)  │     │ • Setiap field punya confidence      │  │
│  │             │     │ • Error OCR sudah dikoreksi          │  │
│  └─────────────┘     └──────────────────────────────────────┘  │
│                                                                  │
│  Analogi: OCR = Mata (baca huruf)                               │
│           AI  = Otak (pahami makna)                             │
└─────────────────────────────────────────────────────────────────┘
```

### Kenapa Tidak Langsung AI Saja Tanpa OCR?

AI (LLM) tidak bisa membaca gambar secara langsung — dia butuh input berupa teks. Jadi OCR tetap diperlukan sebagai "mata" yang mengubah gambar menjadi teks, lalu AI bertindak sebagai "otak" yang memahami dan mengstrukturkan teks tersebut.

Keduanya saling melengkapi:
- **OCR tanpa AI** → bisa baca teks, tapi tidak paham konteks (hanya regex, terbatas)
- **AI tanpa OCR** → pintar tapi buta (tidak bisa baca gambar)
- **OCR + AI** → bisa baca DAN memahami → hasil extraction paling optimal

---

## API Endpoints

| Method | Path | Fungsi |
|--------|------|--------|
| GET | `/` | Serve frontend |
| GET | `/health` | Health check `{ status, ai }` |
| POST | `/extract` | Extract dokumen (multipart/form-data, field: `file`) |

### Response `/extract`

```json
{
  "success": true,
  "file_name": "invoice.png",
  "pages_processed": 1,
  "ocr_confidence": 94.7,
  "extraction_confidence": 90.0,
  "fields_extracted": 14,
  "summary": { "auto_filled": 12, "review_needed": 2, "manual_needed": 0 },
  "fields": [
    { "field": "invoice_number", "value": "INV-2026-00451", "confidence": 90.0, "status": "auto_filled" }
  ],
  "ai": {
    "ai_enabled": true,
    "model": "llama-3.1-8b-instant (Groq)",
    "classification": { "type": "invoice", "confidence": 95 },
    "fields": [...],
    "total_fields": 17
  }
}
```

---

## Demo Script — Beauty Contest (26 Mei 2026)

### Skenario 1: Commercial Invoice (~2 menit)

1. Buka http://localhost:8500
2. Upload `sample-docs/sample_invoice.png`
3. Klik **"Proses Ekstraksi OCR"**
4. Tunjukkan:
   - AI Classification: **"📄 Invoice → BC 2.0 (PIB) bagian Data Invoice"**
   - Summary: 17 fields, semua auto-filled (hijau)
5. Klik tab **"📝 Form"** → form Invoice terisi otomatis
6. Klik tab **"🤖 AI"** → detail model LLaMA 3.1

### Skenario 2: Bill of Lading (~2 menit)

1. Klik **"Reset"**
2. Upload `sample-docs/sample_bill_of_lading.png`
3. Klik **"Proses Ekstraksi OCR"**
4. Tunjukkan:
   - AI Classification: **"🚢 Bill of Lading → BC 2.0 (PIB) bagian Pengangkutan"**
   - **Form BERUBAH** otomatis — sekarang form B/L (Container No, Voyage, dll)
5. Highlight: *"AI otomatis kenali jenis dokumen dan pilih form yang sesuai"*

### Skenario 3 (Opsional): Scan Quality

1. Upload `sample-docs/sample_invoice_scan.jpg` (kualitas lebih rendah)
2. Tunjukkan OCR tetap bisa extract meski kualitas scan rendah
3. Beberapa field berstatus "review" (kuning) — butuh verifikasi manual

### Narasi Penutup

> "Ini POC yang kami bangun untuk menunjukkan pipeline Smart Drafting. Di production, kami akan menggunakan ensemble OCR, model yang di-fine-tune khusus untuk dokumen kepabeanan Indonesia, dan template matching per jenis dokumen. Akurasi akan lebih tinggi lagi dari yang sudah ditunjukkan di sini."

---

## Konfigurasi

### API Key (via UI)

API key Groq sekarang dimasukkan langsung di web UI:
1. Buka http://localhost:8500
2. Klik tombol **⚙️ API Key** di header
3. Masukkan key dari https://console.groq.com/keys
4. Klik Simpan — key tersimpan di browser (localStorage)

### Alternatif: via `.env` file

```bash
# Copy template
cp .env.example .env

# Isi key
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

| Mode | AI Classification | AI Extraction | OCR + Regex | Dynamic Form |
|------|:-:|:-:|:-:|:-:|
| Dengan API Key | ✅ | ✅ | ✅ | ✅ |
| Tanpa API Key | ❌ | ❌ | ✅ | ✅ (default: Invoice) |

---

## Troubleshooting

| Problem | macOS | Windows |
|---------|-------|----------|
| "Backend Offline" di browser | Pastikan `python3 run_web.py` jalan | Pastikan `python run_web.py` jalan |
| Port 8500 sudah dipakai | `lsof -ti:8500 \| xargs kill -9` | `netstat -ano \| findstr :8500` lalu `taskkill /PID <pid> /F` |
| AI tidak aktif | Cek `.env` — key harus mulai `gsk_` | Sama |
| Tesseract not found | `brew install tesseract` | Install dari [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) + tambah ke PATH |
| PDF tidak bisa diproses | `brew install poppler` | Download [poppler-windows](https://github.com/osber/poppler-windows/releases) + tambah `bin/` ke PATH |

---

## POC vs Production

| Aspek | POC (Demo Ini) | Production |
|-------|----------------|---------------------------|
| OCR Engine | Tesseract 5 | Ensemble (Tesseract + PaddleOCR) |
| AI Model | LLaMA 3.1 8B (Groq cloud) | Self-hosted / on-premise LLM |
| Layout Understanding | Regex + LLM prompt | LayoutLM / Donut model |
| Template Matching | Tidak ada | Per document type template |
| Training | Pre-trained only | Fine-tuned on customs docs |
| Continuous Learning | Tidak ada | Feedback loop dari user corrections |
| Scalability | Single thread Flask | Multi-worker + queue (RabbitMQ) |
| Security | Localhost only | OAuth2 + JWT + mTLS |
| Database | Tidak ada | PostgreSQL + MongoDB |
| Frontend | Static HTML | React 18 + TypeScript |

---

## Tim & Kontak

| Role | Tanggung Jawab |
|------|----------------|
| Backend Engineer | Pipeline OCR + AI, arsitektur, strategi akurasi |
| System Analyst | Integrasi ke arsitektur production |
| Project Manager | Konteks keseluruhan, timeline implementasi |
