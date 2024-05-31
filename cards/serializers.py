from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    censored_number = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['censored_number', 'card_number', 'ccv']

    def validate_card_number(self, value):
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("Card number must be 16 digits long and contain only numbers [0-9].")
        return value

    def validate_ccv(self, value):
        if len(value) != 3 or not value.isdigit() or not (100 <= int(value) <= 999):
            raise serializers.ValidationError("CCV must be a three-digit number between 100 and 999.")
        return value

    def get_censored_number(self, obj):
        return obj.card_number[:4] + '*' * 8 + obj.card_number[-4:]

    def validate(self, data):
        card_number = data.get('card_number', '')
        ccv = int(data.get('ccv', ''))

        # Validate card based on the provided logic
        pairs = [(int(card_number[i]), int(card_number[i + 1])) for i in range(0, len(card_number), 2)]
        for x, y in pairs:
            if x ** (y ** 3) % ccv % 2 != 0:
                raise serializers.ValidationError("Invalid card. CCV validation failed.")
        return data
