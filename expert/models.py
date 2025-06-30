from django.db import models

# Create your models here.


class DiagnosaRiwayat(models.Model):
    nama = models.CharField(max_length=100)
    usia = models.IntegerField()
    jenis_kelamin = models.CharField(max_length=10)
    gejala = models.TextField()  # disimpan sebagai teks, bisa pakai join
    hasil = models.CharField(max_length=100)
    saran = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} - {self.hasil}"
