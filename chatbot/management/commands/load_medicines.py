import csv
from django.core.management.base import BaseCommand
from chatbot.models import Medicine

class Command(BaseCommand):
    help = "Load medicine data from a CSV file"

    def handle(self, *args, **kwargs):
        file_path = "FinalMedicineDataset.csv"  # Ensure this file is in the root directory
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Medicine.objects.create(
                        name=row["Medicine Name"].title(),
                        composition=row.get("composition", ""),
                        uses=row.get("uses", ""),
                        side_effects=row.get("side_effects", ""),
                        substitutes=row.get("substitutes", ""),
                        image=row.get("Image URL", "")
                    )
            self.stdout.write(self.style.SUCCESS("Medicine data loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found. Ensure CleanedMedicineDataset.csv exists."))
