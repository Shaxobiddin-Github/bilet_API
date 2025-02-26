from rest_framework import serializers
from .models import SamDUkf, File, Uquv_yili, Bosqich, Talim_yunalishi, Semestr, Fan

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class UquvYiliSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uquv_yili
        fields = '__all__'

class BosqichSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bosqich
        fields = '__all__'

class TalimYunalishiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talim_yunalishi
        fields = '__all__'

class SemestrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestr
        fields = '__all__'

class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = '__all__'

class SamDUkfSerializer(serializers.ModelSerializer):
    uquv_yili = UquvYiliSerializer()
    semestr = SemestrSerializer()
    fan = FanSerializer()
    bosqich = BosqichSerializer()
    talim_yunalishi = TalimYunalishiSerializer()
    file = FileSerializer()

    class Meta:
        model = SamDUkf
        fields = '__all__'
