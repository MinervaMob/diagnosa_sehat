# 🩺 Diagnosa Penyakit Ringan – Django Expert System

Aplikasi web berbasis Django untuk mendiagnosa penyakit ringan berdasarkan gejala yang dipilih pengguna. Sistem menyediakan dua metode: **manual** dan **chatbot interaktif**.

## 📂 Struktur Proyek

```
diagnosa-penyakit/
  ├── manage.py
  ├── requirements.txt
  ├── db.sqlite3
  ├── config/
  ├── expert/
      ├── templates/expert/
      ├── views.py
      ├── models.py
      ├── urls.py
```

## ⚙️ Setup dan Instalasi

1. **Buat virtual environment (env):**
   ```bash
   python -m venv env
   ```

2. **Aktifkan virtual environment:**
   - Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source env/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan server Django:**
   ```bash
   python manage.py runserver
   ```

5. **Akses di browser:**
   ```
   http://localhost:8000/
   ```

## 👨‍⚕️ Fitur Utama

- Input data diri dan gejala secara manual.
- Diagnosa menggunakan chatbot interaktif.
- Penyimpanan riwayat diagnosa ke database.
- Tampilan responsif dan modern (Tailwind CSS).