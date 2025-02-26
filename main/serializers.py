# serializers.py
from rest_framework import serializers
from .models import SamDUkf, File, Uquv_yili, Bosqich, Talim_yunalishi, Semestr, Fan

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file']

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

class SamDUkfSerializer(serializers.ModelSerializer):
    uquv_yili = UquvYiliSerializer(read_only=True)
    semestr = SemestrSerializer(read_only=True)
    fan = FanSerializer(read_only=True)
    bosqich = BosqichSerializer(read_only=True)
    talim_yunalishi = TalimYunalishiSerializer(read_only=True)
    file = FileSerializer(read_only=True)

    uquv_yili_id = serializers.PrimaryKeyRelatedField(queryset=Uquv_yili.objects.all(), source='uquv_yili', write_only=True)
    semestr_id = serializers.PrimaryKeyRelatedField(queryset=Semestr.objects.all(), source='semestr', write_only=True)
    fan_id = serializers.PrimaryKeyRelatedField(queryset=Fan.objects.all(), source='fan', write_only=True)
    bosqich_id = serializers.PrimaryKeyRelatedField(queryset=Bosqich.objects.all(), source='bosqich', write_only=True)
    talim_yunalishi_id = serializers.PrimaryKeyRelatedField(queryset=Talim_yunalishi.objects.all(), source='talim_yunalishi', write_only=True)
    file_id = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), source='file', write_only=True)

    class Meta:
        model = SamDUkf
        fields = [
            'id', 'uquv_yili', 'semestr', 'fan', 'bosqich', 'talim_yunalishi', 'file',
            'biletlar_soni', 'oson_savol', 'urtacha_savol', 'murakkab1', 'murakkab2', 'qiyin_savol',
            'uquv_yili_id', 'semestr_id', 'fan_id', 'bosqich_id', 'talim_yunalishi_id', 'file_id'
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
        if data.get('biletlar_soni') < 1:
            raise serializers.ValidationError({'biletlar_soni': "Biletlar soni kamida 1 bo'lishi kerak!"})
        return data