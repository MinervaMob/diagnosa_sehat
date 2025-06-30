from django.shortcuts import render
from .models import DiagnosaRiwayat
from collections import Counter
from django.http import HttpResponseRedirect
from django.urls import reverse


# Basis Pengetahuan
rules = [
    {
        "conditions": ["demam", "batuk", "pilek"],
        "diagnosis": "Flu",
        "advice": "Istirahat cukup, minum air hangat, dan konsumsi vitamin C.",
        "description": "Flu adalah infeksi virus yang menyerang saluran pernapasan atas dan menyebabkan gejala seperti demam, batuk, dan pilek."
    },
    {
        "conditions": ["demam", "mual", "lemas", "sakit perut"],
        "diagnosis": "Tipes",
        "advice": "Segera ke dokter, konsumsi makanan bersih dan sehat.",
        "description": "Tipes atau demam tifoid adalah infeksi bakteri yang menyebar melalui makanan atau minuman yang terkontaminasi."
    },
    {
        "conditions": ["demam", "batuk", "sesak napas"],
        "diagnosis": "ISPA",
        "advice": "Gunakan masker dan segera periksa ke dokter jika gejala parah.",
        "description": "ISPA adalah infeksi saluran pernapasan akut yang menyerang hidung, tenggorokan, dan paru-paru."
    },
    {
        "conditions": ["mual", "diare", "lemas"],
        "diagnosis": "Diare Akut",
        "advice": "Minum oralit, hindari makanan pedas dan berminyak.",
        "description": "Diare adalah kondisi saat feses menjadi cair dan frekuensi buang air besar meningkat, biasanya akibat infeksi atau makanan."
    },
    {
        "conditions": ["demam", "nyeri sendi", "ruam", "sakit kepala"],
        "diagnosis": "Demam Berdarah",
        "advice": "Segera periksa darah ke puskesmas/RS, dan perbanyak cairan.",
        "description": "Demam berdarah disebabkan oleh virus dengue dan ditularkan melalui gigitan nyamuk Aedes aegypti."
    },
    {
        "conditions": ["sakit tenggorokan", "batuk", "demam"],
        "diagnosis": "Radang Tenggorokan",
        "advice": "Banyak minum air hangat, hindari makanan pedas dan gorengan.",
        "description": "Radang tenggorokan adalah peradangan pada faring akibat infeksi virus atau bakteri."
    },
    {
        "conditions": ["batuk berdahak", "sesak napas", "demam"],
        "diagnosis": "Bronkitis",
        "advice": "Hindari asap rokok, istirahat cukup, dan konsultasikan ke dokter.",
        "description": "Bronkitis adalah peradangan pada saluran bronkus di paru-paru yang menyebabkan batuk berdahak dan sesak napas."
    },
    {
        "conditions": ["nyeri dada", "sesak napas", "lemas"],
        "diagnosis": "Serangan Jantung Ringan",
        "advice": "Segera cari bantuan medis darurat, jangan tunggu lebih lama.",
        "description": "Serangan jantung terjadi saat aliran darah ke jantung terhambat, menyebabkan kerusakan jaringan otot jantung."
    },
    {
        "conditions": ["pusing", "mual", "pandangan kabur"],
        "diagnosis": "Hipotensi",
        "advice": "Perbanyak minum air putih dan konsumsi garam secukupnya.",
        "description": "Hipotensi adalah kondisi tekanan darah rendah yang bisa menyebabkan pusing, lemas, dan penglihatan kabur."
    },
    {
        "conditions": ["sakit kepala", "leher kaku", "demam tinggi"],
        "diagnosis": "Meningitis",
        "advice": "Segera bawa ke rumah sakit, ini kondisi darurat.",
        "description": "Meningitis adalah peradangan pada selaput otak dan sumsum tulang belakang, bisa disebabkan oleh virus atau bakteri."
    },
    {
        "conditions": ["sakit perut", "mual", "kembung"],
        "diagnosis": "Maag",
        "advice": "Makan teratur, hindari kopi dan makanan asam atau pedas.",
        "description": "Maag adalah peradangan lambung yang ditandai dengan nyeri perut, mual, dan perut kembung."
    },
    {
        "conditions": ["frekuensi buang air kecil meningkat", "nyeri saat buang air kecil", "demam"],
        "diagnosis": "Infeksi Saluran Kemih (ISK)",
        "advice": "Minum air putih banyak, hindari menahan pipis.",
        "description": "ISK adalah infeksi pada saluran kemih yang menyebabkan nyeri saat buang air kecil dan frekuensi meningkat."
    },
    {
        "conditions": ["keringat dingin", "tangan gemetar", "lemas"],
        "diagnosis": "Hipoglikemia",
        "advice": "Konsumsi makanan/minuman manis segera, seperti teh manis atau permen.",
        "description": "Hipoglikemia adalah kondisi kadar gula darah rendah yang dapat menyebabkan lemas dan pingsan jika tidak segera ditangani."
    },
    {
        "conditions": ["tenggorokan gatal", "bersin", "mata berair"],
        "diagnosis": "Alergi Ringan",
        "advice": "Hindari pemicu alergi dan konsumsi antihistamin jika perlu.",
        "description": "Alergi ringan bisa disebabkan oleh debu, serbuk bunga, atau makanan tertentu yang menyebabkan bersin dan mata berair."
    },
    {
        "conditions": ["demam", "kehilangan penciuman", "batuk kering"],
        "diagnosis": "Covid-19 Ringan",
        "advice": "Isolasi mandiri, minum vitamin, dan lakukan tes jika diperlukan.",
        "description": "Covid-19 adalah infeksi virus corona yang menyerang sistem pernapasan, bisa ringan hingga berat."
    }
]


# Semua gejala unik
all_gejala = sorted(set(g for r in rules for g in r["conditions"]))


def home(request):
    return render(request, 'expert/home.html', {'gejala': all_gejala})


def diagnosa(request):
    hasil_terbaik = None
    kemungkinan = []

    if request.method == "POST":
        nama = request.POST.get("nama")
        usia = request.POST.get("usia")
        jk = request.POST.get("jenis_kelamin")
        gejala_input = request.POST.getlist("gejala")

        for rule in rules:
            matched = [g for g in rule["conditions"] if g in gejala_input]
            score = len(matched) / len(rule["conditions"]) * 100

            if matched:
                kemungkinan.append({
                    "diagnosis": rule["diagnosis"],
                    "matched": matched,
                    "total_conditions": len(rule["conditions"]),
                    "score": round(score),
                    "advice": rule["advice"],
                    "description": rule.get("description", "-")  # Tambahan ini
                })

        # Ranking berdasarkan skor tertinggi
        kemungkinan.sort(key=lambda x: x["score"], reverse=True)
        hasil_terbaik = kemungkinan[0] if kemungkinan else None

        # Simpan hasil terbaik ke database
        DiagnosaRiwayat.objects.create(
            nama=nama,
            usia=usia,
            jenis_kelamin=jk,
            gejala=", ".join(gejala_input),
            hasil=hasil_terbaik["diagnosis"] if hasil_terbaik else "Tidak diketahui",
            saran=hasil_terbaik["advice"] if hasil_terbaik else "-"
        )

        return render(request, 'expert/hasil.html', {
            'hasil': hasil_terbaik,
            'kemungkinan': kemungkinan,
            'pasien': nama,
            'identitas': {
                'nama': nama,
                'usia': usia,
                'jenis_kelamin': jk
            }
        })

    # Jika bukan POST, kembalikan ke form
    return HttpResponseRedirect(reverse('home'))


def chatbot(request):
    if not request.session.get('identitas'):
        return HttpResponseRedirect(reverse('chatbot_start'))

    gejala_list = all_gejala
    step = request.session.get('chatbot_step', 0)
    jawaban = request.session.get('chatbot_jawaban', {})

    if request.method == 'POST' and 0 < step <= len(gejala_list):
        gejala_sebelumnya = gejala_list[step - 1]
        jawaban[gejala_sebelumnya] = request.POST.get('jawab') == 'ya'
        request.session['chatbot_jawaban'] = jawaban

    input_gejala = [g for g, v in jawaban.items() if v]
    kemungkinan = []
    for rule in rules:
        matched = [g for g in rule["conditions"] if g in input_gejala]
        score = len(matched) / len(rule["conditions"]) * 100
        if matched:
            kemungkinan.append({
                "diagnosis": rule["diagnosis"],
                "matched": matched,
                "score": round(score),
                "advice": rule["advice"],
                "description": rule.get("description", "-")
            })

    # Deteksi dini jika cocok kuat
    early_match = [r for r in kemungkinan if r["score"] >= 70]
    if step >= 3 and early_match:
        hasil = sorted(early_match, key=lambda x: x["score"], reverse=True)[0]
        request.session['chatbot_step'] = 0
        request.session['chatbot_jawaban'] = {}

        return render(request, 'expert/hasil.html', {
            'hasil': hasil,
            'kemungkinan': kemungkinan,
            'pasien': request.session['identitas']['nama'],
            'identitas': request.session['identitas']
        })

    # Masih ada pertanyaan
    if step < len(gejala_list):
        if request.method == 'POST':
            step += 1
            request.session['chatbot_step'] = step
        pertanyaan = gejala_list[step]
        return render(request, 'expert/chatbot.html', {
            'pertanyaan': pertanyaan,
            'step': step + 1,
            'total': len(gejala_list)
        })

    # Selesai semua
    hasil = sorted(kemungkinan, key=lambda x: x["score"], reverse=True)[
        0] if kemungkinan else None
    request.session['chatbot_step'] = 0
    request.session['chatbot_jawaban'] = {}

    return render(request, 'expert/hasil.html', {
        'hasil': hasil,
        'kemungkinan': kemungkinan,
        'pasien': request.session['identitas']['nama'],
        'identitas': request.session['identitas']
    })


def chatbot_start(request):
    if request.method == 'POST':
        request.session['identitas'] = {
            'nama': request.POST.get('nama'),
            'usia': request.POST.get('usia'),
            'jenis_kelamin': request.POST.get('jenis_kelamin')
        }
        request.session['chatbot_step'] = 0
        request.session['chatbot_jawaban'] = {}
        return HttpResponseRedirect(reverse('chatbot'))

    return render(request, 'expert/chatbot_start.html')
