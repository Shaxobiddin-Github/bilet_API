from django.contrib import admin
from .models import SamDUkf, Uquv_yili, Bosqich, Talim_yunalishi, Semestr, Fan, SamDUkfDoc

@admin.register(SamDUkf)
class SamDUkfAdmin(admin.ModelAdmin):
    list_display = ('id', 'uquv_yili', 'semestr', 'fan', 'bosqich', 'talim_yunalishi', 'biletlar_soni')
    search_fields = ('fan__fan', 'uquv_yili__uquv_yili', 'talim_yunalishi__talim_yunalishi')
    list_filter = ('uquv_yili', 'semestr', 'bosqich', 'talim_yunalishi')



@admin.register(Uquv_yili)
class UquvYiliAdmin(admin.ModelAdmin):
    list_display = ('id', 'uquv_yili')
    search_fields = ('uquv_yili',)

@admin.register(Bosqich)
class BosqichAdmin(admin.ModelAdmin):
    list_display = ('id', 'bosqich')
    search_fields = ('bosqich',)

@admin.register(Talim_yunalishi)
class TalimYunalishiAdmin(admin.ModelAdmin):
    list_display = ('id', 'talim_yunalishi')
    search_fields = ('talim_yunalishi',)

@admin.register(Semestr)
class SemestrAdmin(admin.ModelAdmin):
    list_display = ('id', 'semestr')
    search_fields = ('semestr',)

@admin.register(Fan)
class FanAdmin(admin.ModelAdmin):
    list_display = ('id', 'fan')
    search_fields = ('fan',)

@admin.register(SamDUkfDoc)
class SamDUkfDocAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
    search_fields = ('file',)
