from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    # ბაზიდან წაკითხვის დროს საჭიროა რომ არ მოითხოვოს ამ ველების წამოღებაც რომელიც არ არის ბაზაში  შენახული write_only
    card_number = serializers.CharField(max_length=16, write_only=True)
    ccv = serializers.CharField(max_length=3, write_only=True)

    class Meta:
        model = Card
        fields = ['title','censored_number','card_number', 'ccv']
        # post მეთოდის დროს censored_number-ს ითხოვდა რომ შევსებულიყო, read_only_fields აგვარებს ამ საკითხს
        read_only_fields = ['title', 'censored_number']
        
    def validate_card_number(self, value):
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("Card number must be 16 digits long and contain only numbers [0-9].")
        return value

    def validate_ccv(self, value):
        if len(value) != 3 or not value.isdigit() or not (100 <= int(value) <= 999):
            raise serializers.ValidationError("CCV must be a three-digit number between 100 and 999.")
        return value

    def get_censored_number(self, card_number):
        return card_number[:4] + '*' * 8 + card_number[-4:]

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        ccv = validated_data.pop('ccv')
        user = self.context['request'].user if 'request' in self.context and self.context['request'].user.is_authenticated else None

        validated_data['censored_number'] = self.get_censored_number(card_number)
        validated_data['is_valid'] = True
        validated_data['title'] = 'visa'
        validated_data['user'] = user
        return super().create(validated_data)
