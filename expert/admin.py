from django.contrib import admin
from .models import DiagnosaRiwayat


@admin.register(DiagnosaRiwayat)
class DiagnosaRiwayatAdmin(admin.ModelAdmin):
    list_display = ('nama', 'usia', 'jenis_kelamin', 'hasil', 'waktu')
    list_filter = ('jenis_kelamin', 'hasil')
    search_fields = ('nama', 'hasil', 'gejala')
    ordering = ('-waktu',)
    readonly_fields = ('waktu',)

    fieldsets = (
        (None, {
            'fields': ('nama', 'usia', 'jenis_kelamin', 'gejala', 'hasil', 'saran', 'waktu')
        }),
    )

    save_as = True
    save_on_top = True
