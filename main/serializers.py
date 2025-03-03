from rest_framework import serializers
from .models import SamDUkf,  SamDUkfDoc, Uquv_yili, Bosqich, Talim_yunalishi, Semestr, Fan



class UquvYiliSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uquv_yili
        fields = ['id', 'uquv_yili']

class BosqichSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bosqich
        fields = ['id', 'bosqich']

class TalimYunalishiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talim_yunalishi
        fields = ['id', 'talim_yunalishi']

class SemestrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestr
        fields = ['id', 'semestr']

class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = ['id', 'fan']


class SamDUkfDocSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = SamDUkfDoc
        fields = ['id', 'samdukf', 'file', 'file_url']  # Fayl URL manzilini ham qo'shildi
        read_only_fields = ['id']

    def get_file_url(self, obj):
        """
        Faylning to'liq URL manzilini qaytaradi.
        """
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

    def validate_file(self, value):
        """
        Fayl uchun validatsiya (masalan, hajmi yoki turi bo'yicha).
        """
        if value.size > 10 * 1024 * 1024:  # 10 MB dan katta bo'lmasligi uchun
            raise serializers.ValidationError("Fayl hajmi 10 MB dan oshmasligi kerak.")
        return value


class SamDUkfSerializer(serializers.ModelSerializer):
    # Bog'langan modellarni o'qish uchun StringRelatedField
    uquv_yili = serializers.StringRelatedField(read_only=True)
    semestr = serializers.StringRelatedField(read_only=True)
    fan = serializers.StringRelatedField(read_only=True)
    bosqich = serializers.StringRelatedField(read_only=True)
    talim_yunalishi = serializers.StringRelatedField(read_only=True)

    # Bog'langan modellarga ID orqali yozish uchun PrimaryKeyRelatedField
    uquv_yili_id = serializers.PrimaryKeyRelatedField(
        queryset=Uquv_yili.objects.all(),
        source='uquv_yili',
        write_only=True
    )
    semestr_id = serializers.PrimaryKeyRelatedField(
        queryset=Semestr.objects.all(),
        source='semestr',
        write_only=True
    )
    fan_id = serializers.PrimaryKeyRelatedField(
        queryset=Fan.objects.all(),
        source='fan',
        write_only=True
    )
    bosqich_id = serializers.PrimaryKeyRelatedField(
        queryset=Bosqich.objects.all(),
        source='bosqich',
        write_only=True
    )
    talim_yunalishi_id = serializers.PrimaryKeyRelatedField(
        queryset=Talim_yunalishi.objects.all(),
        source='talim_yunalishi',
        write_only=True
    )

    # Bog'langan SamDUkfDoc obyektlarini ko'rsatish
    samdukfdoc = SamDUkfDocSerializer(read_only=True)

    # Fayl uchun serializer maydoni
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = SamDUkf
        fields = [
            'id',
            'uquv_yili', 'semestr', 'fan', 'bosqich', 'talim_yunalishi',
            'file',
            'biletlar_soni', 'oson_savol', 'urtacha_savol', 'murakkab1', 'murakkab2', 'qiyin_savol',
            'uquv_yili_id', 'semestr_id', 'fan_id', 'bosqich_id', 'talim_yunalishi_id',
            'samdukfdoc'  # Bog'langan SamDUkfDoc obyektlari
        ]

    def validate(self, data):
        # Savollar sonini 1-5 oralig'ida tekshirish
        for field, value in [
            ('oson_savol', data.get('oson_savol')),
            ('urtacha_savol', data.get('urtacha_savol')),
            ('murakkab1', data.get('murakkab1')),
            ('murakkab2', data.get('murakkab2')),
            ('qiyin_savol', data.get('qiyin_savol'))
        ]:
            if not (1 <= value <= 5):
                raise serializers.ValidationError({field: f"{field} 1 dan 5 gacha bo'lishi kerak!"})

        # Biletlar sonini tekshirish
        if data.get('biletlar_soni') < 1:
            raise serializers.ValidationError({'biletlar_soni': "Biletlar soni kamida 1 bo'lishi kerak!"})

        return data