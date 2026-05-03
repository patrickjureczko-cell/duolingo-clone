from django.core.management.base import BaseCommand
from topics.models import Topic

TOPICS = [
    {'name': 'IT & Technology', 'icon': '💻', 'description': 'Computer science, networking, programming, and software.', 'color': '#1CB0F6'},
    {'name': 'Dentistry', 'icon': '🦷', 'description': 'Oral health, dental procedures, and tooth anatomy.', 'color': '#FF9600'},
    {'name': 'Mechanics', 'icon': '🔧', 'description': 'Automotive systems, repairs, and engineering principles.', 'color': '#FF4B4B'},
    {'name': 'Medicine', 'icon': '🏥', 'description': 'Human anatomy, diseases, pharmacology, and clinical practice.', 'color': '#58CC02'},
    {'name': 'Business & Finance', 'icon': '📊', 'description': 'Accounting, economics, marketing, and management.', 'color': '#CE82FF'},
    {'name': 'Law', 'icon': '⚖️', 'description': 'Legal principles, case law, contracts, and procedure.', 'color': '#FF9600'},
    {'name': 'Engineering', 'icon': '🏗️', 'description': 'Civil, mechanical, electrical, and chemical engineering.', 'color': '#1CB0F6'},
    {'name': 'Culinary Arts', 'icon': '🍳', 'description': 'Cooking techniques, nutrition, and food science.', 'color': '#FF4B4B'},
]


class Command(BaseCommand):
    help = 'Seed the database with default topics'

    def handle(self, *args, **options):
        created = 0
        for data in TOPICS:
            _, is_new = Topic.objects.get_or_create(name=data['name'], defaults=data)
            if is_new:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Done. {created} new topic(s) created.'))
