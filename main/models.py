from django.db import models

class SamDUkf(models.Model):
    """
    Ushbu model akademik yil, semestr, fan, bosqich va mutaxassislik bo'yicha
    ma'lumotlarni saqlash uchun ishlatiladi.
    """
    uquv_yili = models.ForeignKey("Uquv_yili", on_delete=models.CASCADE)
    semestr = models.ForeignKey("Semestr", on_delete=models.CASCADE)
    fan = models.ForeignKey("Fan", on_delete=models.CASCADE)
    bosqich = models.ForeignKey("Bosqich", on_delete=models.CASCADE)
    talim_yunalishi = models.ForeignKey("Talim_yunalishi", on_delete=models.CASCADE)
    file = models.ForeignKey("File", on_delete=models.CASCADE)
    biletlar_soni = models.IntegerField(default=1, help_text="nechta bilet kerakligini kiriting?")
    oson_savol = models.IntegerField(default=1, help_text="oson savollar")
    urtacha_savol = models.IntegerField(default=1, help_text="urtacha darajali savollar")
    murakkab1 = models.IntegerField(default=1, help_text="murakkab1 darajaga mansub savollar")
    murakkab2 = models.IntegerField(default=1, help_text="murakkab2 darajaga mansub savollar")
    qiyin_savol = models.IntegerField(default=1, help_text = "eng qiyin savollar tuplami")

    

    def __str__(self):
        return f"{self.fan} ({self.uquv_yili})"


class File(models.Model):
    """
    Ushbu model hujjatlarni saqlash uchun ishlatiladi.
    """
    file = models.FileField(upload_to='documents/', help_text="Yuklangan fayl")

    def __str__(self):
        return f"Fayl: {self.file.name}"

class Uquv_yili(models.Model):
    """
    Ushbu model o'quv yili bo'yicha ma'lumotlarni saqlash uchun ishlatiladi.
    """
    uquv_yili = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.uquv_yili}"
    
class Bosqich(models.Model):
    """
    Ushbu model bosqich raqamini saqlash uchun ishlatiladi.
    """
    bosqich = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.bosqich}"
    

class Talim_yunalishi(models.Model):
    """
    Ushbu model mutaxassislik nomini saqlash uchun ishlatiladi.
    """
    talim_yunalishi = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.talim_yunalishi.capitalize()}"
    
class Semestr(models.Model):
    """
    Ushbu model semestr nomini saqlash uchun ishlatiladi.
    """
    semestr = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.semestr}"
    
class Fan(models.Model):
    """
    Ushbu model fan nomini saqlash uchun ishlatiladi.
    """
    fan = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.fan.capitalize()}"
    

