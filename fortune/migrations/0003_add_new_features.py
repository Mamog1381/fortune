# Generated manually for new features: foot_reading, istikhara, ramal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fortune', '0002_add_language_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fortunefeature',
            name='feature_type',
            field=models.CharField(
                choices=[
                    ('coffee_fortune', 'Coffee Fortune Reading'),
                    ('feng_shui', 'Feng Shui Analysis'),
                    ('dream_interpretation', 'Dream Interpretation'),
                    ('birthdate_horoscope', 'Birthdate Horoscope'),
                    ('tarot', 'Tarot Reading'),
                    ('numerology', 'Numerology'),
                    ('palm_reading', 'Palm Reading'),
                    ('foot_reading', 'Foot Reading / طالع بینی فرم پا'),
                    ('istikhara', 'Istikhara / استخاره'),
                    ('ramal', 'Geomancy (Ramal) / رمال'),
                ],
                max_length=50,
                unique=True
            ),
        ),
    ]
