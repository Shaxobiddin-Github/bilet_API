import requests
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import SamDUkf, SamDUkfDoc
from django.core.files.storage import default_storage




@receiver(post_save, sender=SamDUkf)
def upload_questions_after_samd_ukf_creation(sender, instance, created, **kwargs):
    """
    Yangi SamDUkf yozuvi qo'shilganda, avtomatik ravishda UploadQuestions API ga POST so'rovi yuboriladi.
    """
    if created:  # Faqat yangi yozuv qo'shilganda ishlaydi
        try:
            # UploadQuestions API manzili
            upload_url = "http://127.0.0.1:8000/api/upload/"  # URL manzilini to'g'rilang
            # POST so'rovi yuborish (token kerak emas, chunki AllowAny ishlatilmoqda)
            response = requests.post(upload_url)

            

            # Agar xatolik bo'lsa, logga yozamiz
            if response.status_code != 200:
                print(f"Xatolik: UploadQuestions API ga so'rov yuborishda muammo. Status code: {response.status_code}, Xabar: {response.text}")
        except Exception as e:
            print(f"Signal ishlashida xatolik: {str(e)}")


from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import SamDUkfDoc

@receiver(pre_save, sender=SamDUkfDoc)
def delete_old_files(sender, instance, **kwargs):
    """
    Yangi fayl qo'shilganda eski fayllarni o'chiradi.
    """
    if instance.pk:  # Agar ob'ekt allaqachon mavjud bo'lsa (yangilanish holati)
        try:
            old_instance = SamDUkfDoc.objects.get(pk=instance.pk)
            # Agar eski fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa
            if old_instance.file and old_instance.file != instance.file:
                old_instance.file.delete(save=False)  # Eski faylni o'chirish
        except SamDUkfDoc.DoesNotExist:
            pass  # Agar ob'ekt topilmasa, hech narsa qilmaymiz
    else:  # Agar yangi ob'ekt yaratilayotgan bo'lsa
        # Shu `samdukf` bilan bog'liq barcha eski fayllarni o'chirish
        SamDUkfDoc.objects.filter(samdukf=instance.samdukf).delete()