from django.core.management.base import BaseCommand
from topics.models import Topic

TOPICS = [
    {'name': 'IT & Technologie', 'icon': '💻', 'description': 'Informatik, Netzwerke, Programmierung und Software.', 'color': '#1CB0F6'},
    {'name': 'Zahnmedizin', 'icon': '🦷', 'description': 'Mundhygiene, zahnmedizinische Eingriffe und Zahnanatomie.', 'color': '#FF9600'},
    {'name': 'Kfz-Technik', 'icon': '🔧', 'description': 'Fahrzeugsysteme, Reparaturen und technische Grundlagen.', 'color': '#FF4B4B'},
    {'name': 'Medizin', 'icon': '🏥', 'description': 'Anatomie, Krankheiten, Pharmakologie und klinische Praxis.', 'color': '#58CC02'},
    {'name': 'BWL & Finanzen', 'icon': '📊', 'description': 'Buchhaltung, Volkswirtschaft, Marketing und Management.', 'color': '#CE82FF'},
    {'name': 'Rechtswesen', 'icon': '⚖️', 'description': 'Rechtsgrundsätze, Fallrecht, Verträge und Verfahren.', 'color': '#FF9600'},
    {'name': 'Ingenieurwesen', 'icon': '🏗️', 'description': 'Bau-, Maschinen-, Elektro- und Verfahrenstechnik.', 'color': '#1CB0F6'},
    {'name': 'Kulinarik', 'icon': '🍳', 'description': 'Kochtechniken, Ernährungslehre und Lebensmittelkunde.', 'color': '#FF4B4B'},
]


class Command(BaseCommand):
    help = 'Standardthemen in die Datenbank eintragen'

    def handle(self, *args, **options):
        created = 0
        for data in TOPICS:
            _, is_new = Topic.objects.get_or_create(name=data['name'], defaults=data)
            if is_new:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Fertig. {created} neues Thema/neue Themen erstellt.'))
