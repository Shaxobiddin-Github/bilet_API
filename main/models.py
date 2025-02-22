from django.db import models

class SamDUkf(models.Model):
    """
    Ushbu model akademik yil, semestr, fan, bosqich va mutaxassislik bo'yicha
    ma'lumotlarni saqlash uchun ishlatiladi.
    """
    academic_year = models.IntegerField(default=2025, help_text="Akademik yil (masalan, 2025)")
    semester = models.CharField(max_length=10, help_text="Semestr nomi (masalan, 'Bahor', 'Kuz')")
    subject = models.CharField(max_length=200, help_text="Fan nomi")
    stage = models.IntegerField(default=0, help_text="Bosqich (kurs) raqami")
    field_of_study = models.CharField(max_length=55, help_text="Ta'lim yo'nalishi")

    def __str__(self):
        return f"{self.subject} ({self.academic_year})"


class File(models.Model):
    """
    Ushbu model hujjatlarni saqlash uchun ishlatiladi.
    """
    file = models.FileField(upload_to='documents/', help_text="Yuklangan fayl")

    def __str__(self):
        return f"Fayl: {self.file.name}"
