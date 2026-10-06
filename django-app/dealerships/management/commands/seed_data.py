from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dealerships.models import CarMake, CarModel
import os

class Command(BaseCommand):
    help = 'Crea el superusuario root y siembra marcas y modelos de automóviles'

    def handle(self, *args, **options):
        # 1. Create root superuser if not exists
        root_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'root')
        root_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'root@autopulse.com')
        root_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'rootpassword123')

        if not User.objects.filter(username=root_username).exists():
            User.objects.create_superuser(
                username=root_username,
                email=root_email,
                password=root_password
            )
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{root_username}' creado con éxito."))
        else:
            self.stdout.write(self.style.WARNING(f"Superusuario '{root_username}' ya existe."))

        # 2. Seed Car Makes & Models
        cars_data = {
            "Toyota": {
                "desc": "Fabricante japonés reconocido mundialmente por su fiabilidad e innovación híbrida.",
                "models": [
                    ("Camry", "SEDAN", 2023, 1),
                    ("Corolla", "SEDAN", 2024, 1),
                    ("RAV4", "SUV", 2024, 2),
                    ("Highlander", "SUV", 2023, 3)
                ]
            },
            "Honda": {
                "desc": "Compañía multinacional conocida por su ingeniería eficiente y durabilidad.",
                "models": [
                    ("Civic", "SEDAN", 2022, 1),
                    ("Accord", "SEDAN", 2023, 2),
                    ("CR-V", "SUV", 2024, 4)
                ]
            },
            "Ford": {
                "desc": "Pionero estadounidense en automoción, famoso por sus pickups y muscle cars.",
                "models": [
                    ("F-150", "PICKUP", 2023, 1),
                    ("Mustang", "COUPE", 2024, 3),
                    ("Explorer", "SUV", 2023, 2)
                ]
            },
            "BMW": {
                "desc": "Fabricante alemán premium enfocado en dinámica de conducción y lujo deportivo.",
                "models": [
                    ("3 Series", "SEDAN", 2024, 2),
                    ("X5", "SUV", 2024, 2),
                    ("M4", "COUPE", 2023, 5)
                ]
            },
            "Chevrolet": {
                "desc": "División de General Motors especializada en SUVs robustos y utilitarios.",
                "models": [
                    ("Tahoe", "SUV", 2023, 3),
                    ("Silverado", "PICKUP", 2024, 3),
                    ("Corvette", "COUPE", 2024, 5)
                ]
            }
        }

        for make_name, info in cars_data.items():
            make, created = CarMake.objects.get_or_create(
                name=make_name,
                defaults={'description': info['desc']}
            )
            if created:
                self.stdout.write(f"Marca creada: {make_name}")
            
            for model_name, car_type, year, dealer_id in info['models']:
                model_obj, m_created = CarModel.objects.get_or_create(
                    make=make,
                    name=model_name,
                    defaults={'type': car_type, 'year': year, 'dealer_id': dealer_id}
                )
                if m_created:
                    self.stdout.write(f"  - Modelo creado: {model_name}")

        self.stdout.write(self.style.SUCCESS("Semilla de base de datos completada exitosamente."))
