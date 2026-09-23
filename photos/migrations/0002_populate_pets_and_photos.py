from datetime import date

from django.db import migrations
from django.utils.text import slugify


PETS = [
    ("Max", date(2019, 4, 12)),
    ("Bella", date(2020, 7, 3)),
    ("Luna", date(2021, 1, 25)),
    ("Charlie", date(2018, 11, 8)),
    ("Milo", date(2022, 3, 17)),
    ("Daisy", date(2017, 9, 30)),
    ("Rocky", date(2020, 12, 1)),
    ("Coco", None),
    ("Oscar", date(2023, 5, 14)),
    ("Nala", date(2021, 8, 22)),
    ("Axel", None),
]

PHOTOS = [
    ("photos/max-beach.jpg", "Max chasing waves on a sunny afternoon.", "Varna", ["Max"]),
    ("photos/bella-park.jpg", "Bella found the biggest stick in the park.", "Sofia", ["Bella"]),
    ("photos/luna-window.jpg", "Luna watching the snow fall from the window.", "Plovdiv", ["Luna"]),
    ("photos/charlie-hike.jpg", "Charlie reached the summit before all of us!", "Vitosha", ["Charlie"]),
    ("photos/milo-nap.jpg", "Milo taking his fifth nap of the day.", "Burgas", ["Milo"]),
    ("photos/daisy-garden.jpg", "Daisy sniffing the spring flowers.", "Ruse", ["Daisy"]),
    ("photos/rocky-bella-play.jpg", "Rocky and Bella playing tug of war.", "Sofia", ["Rocky", "Bella"]),
    ("photos/coco-bath.jpg", "Coco was not a fan of bath time today.", "Stara Zagora", ["Coco"]),
    ("photos/oscar-first-day.jpg", "Oscar's first day in his new home.", "Veliko Tarnovo", ["Oscar"]),
    ("photos/nala-luna-sofa.jpg", "Nala and Luna sharing the sofa for once.", "Plovdiv", ["Nala", "Luna"]),
    ("photos/axel-aquarium.jpg", "Axel smiling at the camera from his tank.", "Bansko", ["Axel"]),
    ("photos/pack-walk.jpg", "Morning walk with the whole gang.", "Borovets", ["Max", "Charlie", "Rocky"]),
]


def populate(apps, schema_editor):
    Pet = apps.get_model("pets", "Pet")
    Photo = apps.get_model("photos", "Photo")

    pets = {}
    for name, date_of_birth in PETS:
        pet = Pet.objects.create(
            name=name,
            personal_photo=f"https://picsum.photos/seed/{name.lower()}/400/400",
            date_of_birth=date_of_birth,
            slug=f"tmp-{name.lower()}",
        )
        # Historical models skip Pet.save(), so build the slug the same way it does, once pk exists.
        pet.slug = slugify(f"{pet.name}-{pet.pk}")
        pet.save(update_fields=["slug"])
        pets[name] = pet

    for photo, description, location, tagged in PHOTOS:
        obj = Photo.objects.create(photo=photo, description=description, location=location)
        obj.tagged_pets.set(pets[name] for name in tagged)


def depopulate(apps, schema_editor):
    Pet = apps.get_model("pets", "Pet")
    Photo = apps.get_model("photos", "Photo")

    Photo.objects.filter(photo__in=[p[0] for p in PHOTOS]).delete()
    Pet.objects.filter(name__in=[p[0] for p in PETS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pets", "0001_initial"),
        ("photos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate, depopulate),
    ]
