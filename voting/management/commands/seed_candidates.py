from django.core.management.base import BaseCommand
from voting.models import Candidate


CANDIDATES = [
    ("TAMMINANA BHARGAV", "PEOPLE RISING PARTY", "images/c1.webp"),
    ("CHAITANYA REDDY", "PEOPLE HAND", "images/c2.webp"),
    ("VISHNU", "THE RISERS", "images/c3.avif"),
    ("RAMA KRISHNA", "THE DEMOCRACY", "images/c4.jpg"),
]


class Command(BaseCommand):
    help = "Create/update the demo candidates."

    def handle(self, *args, **options):
        for name, party, image in CANDIDATES:
            Candidate.objects.update_or_create(
                name=name,
                defaults={"party": party, "image": image, "active": True},
            )
        self.stdout.write(self.style.SUCCESS("Demo candidates are ready."))
