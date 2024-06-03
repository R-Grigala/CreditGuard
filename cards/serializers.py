from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    # ბაზიდან წაკითხვის დროს საჭიროა რომ არ მოითხოვოს ამ ველების წამოღებაც რომელიც არ არის ბაზაში  შენახული write_only
    card_number = serializers.CharField(max_length=16, write_only=True)
    ccv = serializers.CharField(max_length=3, write_only=True)

    class Meta:
        model = Card
        fields = ['title','censored_number', 'creation_date', 'card_number', 'ccv']
        # post მეთოდის დროს censored_number-ს ითხოვდა რომ შევსებულიყო, read_only_fields აგვარებს ამ საკითხს
        # card_number-სა და ccv  არ ვინახავთ ბაზაში
        read_only_fields = ['title', 'censored_number', 'creation_date']
        
    def validate_card_number(self, value):
        # card_number (length) 16 ზომა უნდა იყოს და შეიცავდეს მხოლოდ ციფრებს [0-9].
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("Card number must be 16 digits long and contain only numbers [0-9].")
        
        # დავყოთ მიყოლებით ორ ნიშნა ორ-ორ წყვილებათ
        pairs = []
        for i in range(0, len(value), 2):
            pair = value[i:i+2]
            pairs.append(int(pair))

        paired_numbers = []
        for i in range(0, len(pairs), 2):
            paired_numbers.append((pairs[i], pairs[i+1]))
        
        # ვამოწმებთ card_number-ის რიცხვების სისწორეს (x, y), x^(y^3) % ccv თუ არის ლუწი
        ccv = int(self.initial_data.get('ccv', 0))
        for x, y in paired_numbers:
            # ხარისხში აყვანის ფუნქცია pow
            result = pow(x, pow(y, 3), ccv)
            if result % 2 != 0:
                raise serializers.ValidationError("Card number is invalid. Try again")

        return value

    # ccv – [100, 999] უნდა იყოს სამნიშნა რიცხვი შუალედში
    def validate_ccv(self, value):
        if len(value) != 3 or not value.isdigit() or not (100 <= int(value) <= 999):
            raise serializers.ValidationError("CCV must be a three-digit number between 100 and 999.")
        return value

    # ბაზაში censored_number -ის ფორმატი არის censored_number -ის პირველი ოთხი და ბოლო ოთხი ციფრი ხილული,
    # დანარჩენი კი, ფიფქებით შევსებული
    def get_censored_number(self, card_number):
        return card_number[:4] + '*' * 8 + card_number[-4:]

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        user = self.context['request'].user if 'request' in self.context and self.context['request'].user.is_authenticated else None

        validated_data['censored_number'] = self.get_censored_number(card_number)
        validated_data['is_valid'] = True
        validated_data['title'] = 'visa'
        validated_data['user'] = user
        return super().create(validated_data)
