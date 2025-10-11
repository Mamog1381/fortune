from django.core.management.base import BaseCommand
from fortune.models import FortuneFeature


class Command(BaseCommand):
    help = 'Populate initial fortune features with prompt templates'

    def handle(self, *args, **options):
        features_data = [
            {
                'name': 'Coffee Fortune Reading',
                'feature_type': 'coffee_fortune',
                'input_type': 'image',
                'description': 'Upload a photo of your coffee cup and receive a mystical fortune reading based on the patterns in your coffee grounds.',
                'prompt_template': '''You are an experienced coffee fortune teller (tasseographer).
Analyze the patterns, shapes, and symbols you see in this coffee cup image.

Provide a detailed and engaging fortune reading that includes:
1. **What I See**: Describe 3-4 specific patterns or symbols you observe in the cup
2. **Love & Relationships**: Insights about romantic life and connections
3. **Career & Finance**: Guidance about work and financial matters
4. **Health & Well-being**: Advice about physical and mental health
5. **Near Future**: What the next few weeks may bring
6. **Guidance**: A meaningful piece of advice or warning

Be creative, mystical, and positive while maintaining an entertaining tone. The reading should feel personal and insightful.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1200,
                'temperature': 0.8,
                'credit_cost': 2,
            },
            {
                'name': 'Feng Shui Room Analysis',
                'feature_type': 'feng_shui',
                'input_type': 'image',
                'description': 'Upload a photo of any room in your home and receive personalized Feng Shui advice to improve energy flow and harmony.',
                'prompt_template': '''You are a Feng Shui master with deep knowledge of energy flow (Chi) and spatial harmony.

Analyze this room image and provide comprehensive Feng Shui guidance:

1. **Overall Energy Assessment**: Describe the current energy flow in this space
2. **Positive Elements**: Identify what's working well (colors, placement, natural elements)
3. **Areas for Improvement**: Point out blocking or negative energy patterns
4. **Specific Recommendations**:
   - Furniture placement suggestions
   - Color recommendations
   - Element balance (Water, Wood, Fire, Earth, Metal)
   - Lighting and natural light optimization
5. **Quick Wins**: 3-5 easy changes that can be implemented immediately
6. **Long-term Enhancements**: Bigger changes for maximum benefit

Be practical, specific, and encouraging. Focus on creating harmony and positive energy.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1500,
                'temperature': 0.7,
                'credit_cost': 2,
            },
            {
                'name': 'Dream Interpretation',
                'feature_type': 'dream_interpretation',
                'input_type': 'text',
                'description': 'Share your dream and receive an in-depth interpretation revealing hidden meanings and insights.',
                'prompt_template': '''You are an expert dream interpreter with knowledge of symbolism, psychology, and mystical traditions.

The dreamer shares: {user_input}

Provide a comprehensive dream interpretation:

1. **Dream Summary**: Briefly recap the key elements
2. **Main Symbols**: Identify and explain 3-5 significant symbols or themes
3. **Emotional Undercurrents**: What emotions or subconscious feelings does this dream reveal?
4. **Psychological Meaning**: Insights from a psychological perspective
5. **Spiritual/Mystical Significance**: Deeper spiritual or universal meanings
6. **Personal Reflection Questions**: 3-4 questions to help the dreamer gain deeper insight
7. **Guidance**: Practical advice based on the dream's message

Be thoughtful, insightful, and respectful. Consider both psychological and mystical interpretations.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1200,
                'temperature': 0.75,
                'credit_cost': 1,
            },
            {
                'name': 'Birthdate Horoscope',
                'feature_type': 'birthdate_horoscope',
                'input_type': 'text',
                'description': 'Enter your birthdate to receive personalized insights about your personality, strengths, and life path.',
                'prompt_template': '''You are an expert astrologer and numerologist.

Birthdate provided: {user_input}

Create a detailed personalized reading based on this birthdate:

1. **Sun Sign Overview**: Key traits and characteristics
2. **Life Path Number**: Calculate and explain the numerological significance
3. **Personality Strengths**: Natural talents and positive qualities
4. **Growth Areas**: Challenges and opportunities for development
5. **Career Inclinations**: Suitable career paths and work styles
6. **Relationship Style**: How they love and connect with others
7. **Lucky Elements**: Colors, numbers, days, and stones
8. **Current Period Guidance**: Insights for the present life phase

Be personalized, positive, and insightful. Help the person understand themselves better.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1400,
                'temperature': 0.7,
                'credit_cost': 1,
            },
            {
                'name': 'Tarot Reading',
                'feature_type': 'tarot',
                'input_type': 'text',
                'description': 'Ask a question and receive guidance through a virtual three-card tarot reading.',
                'prompt_template': '''You are an experienced tarot reader with intuitive wisdom.

Question asked: {user_input}

Perform a three-card reading (Past-Present-Future spread):

1. **Card Draw**: Select three cards that resonate with this question
   - Card 1 (Past): [Card Name] - What led to this situation
   - Card 2 (Present): [Card Name] - Current energies and influences
   - Card 3 (Future): [Card Name] - Likely outcome and guidance

2. **Detailed Interpretation**:
   - Explain each card's traditional meaning
   - Connect the cards to the question
   - Describe how the cards interact with each other

3. **Overall Message**: The reading's combined wisdom

4. **Advice**: Actionable guidance based on the reading

5. **Reflection**: A question to help deepen the insight

Be mystical, wise, and supportive. Use actual tarot card names and meanings.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1300,
                'temperature': 0.8,
                'credit_cost': 1,
            },
            {
                'name': 'Numerology Analysis',
                'feature_type': 'numerology',
                'input_type': 'text',
                'description': 'Enter your full name and birthdate for a complete numerology profile.',
                'prompt_template': '''You are a master numerologist with deep understanding of number vibrations.

Information provided: {user_input}

Create a comprehensive numerology reading:

1. **Life Path Number**: Calculate and interpret
2. **Expression Number**: From full name - your natural talents
3. **Soul Urge Number**: Inner desires and motivations
4. **Personality Number**: How others perceive you
5. **Birthday Number**: Special gifts from your birth day

6. **Number Meanings**: Detailed explanation of your core numbers

7. **Life Cycles**: Current phase and what it means

8. **Personal Year**: What this year holds for you

9. **Karmic Lessons**: Numbers missing from your chart and what to learn

10. **Guidance**: How to align with your numbers' energy

Be detailed, accurate with numerology calculations, and insightful.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1600,
                'temperature': 0.7,
                'credit_cost': 2,
            },
            {
                'name': 'Palm Reading',
                'feature_type': 'palm_reading',
                'input_type': 'image',
                'description': 'Upload a clear photo of your palm to receive a detailed palmistry reading.',
                'prompt_template': '''You are a skilled palmist (chiromancer) with expertise in reading hands.

Analyze this palm image and provide a detailed reading:

1. **Hand Shape & Type**: Identify the hand type (Earth, Air, Fire, Water)

2. **Major Lines Analysis**:
   - Heart Line: Love, emotions, relationships
   - Head Line: Intellect, decision-making, mental approach
   - Life Line: Vitality, life changes, physical health
   - Fate Line: Career, life purpose, destiny (if present)

3. **Mounts**: Examine the mounts (Venus, Jupiter, Saturn, etc.) and their meanings

4. **Fingers**: Length, shape, and what they reveal

5. **Special Markings**: Identify stars, crosses, triangles, or other significant marks

6. **Overall Reading**:
   - Personality traits
   - Talents and abilities
   - Relationship patterns
   - Career indicators
   - Health considerations
   - Life path insights

7. **Guidance**: Advice based on palm characteristics

Be detailed, traditional in palmistry knowledge, and encouraging.''',
                'model_name': 'openai/gpt-4o-mini',
                'max_tokens': 1500,
                'temperature': 0.75,
                'credit_cost': 2,
            },
        ]

        created_count = 0
        updated_count = 0

        for feature_data in features_data:
            feature, created = FortuneFeature.objects.update_or_create(
                feature_type=feature_data['feature_type'],
                defaults=feature_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {feature.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated: {feature.name}')
                )

        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )
        self.stdout.write(
            f'Total features in database: {FortuneFeature.objects.count()}\n'
        )
