# Generated manually for language support
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fortune', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fortunefeature',
            name='model_name',
            field=models.CharField(
                default='google/gemini-2.0-flash-exp:free',
                help_text='OpenRouter.ai model identifier',
                max_length=100
            ),
        ),
        migrations.AddField(
            model_name='reading',
            name='language',
            field=models.CharField(
                choices=[('en', 'English'), ('fa', 'Persian (Farsi)')],
                default='en',
                help_text='Language for the interpretation',
                max_length=5
            ),
        ),
    ]
