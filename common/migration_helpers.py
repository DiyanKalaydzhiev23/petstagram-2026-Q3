from django.conf import settings
from django.db import migrations

PLACEHOLDER_OWNER_EMAIL = "owner@petstagram.local"


def _get_default_owner(apps):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    UserModel = apps.get_model(app_label, model_name)

    owner = UserModel.objects.order_by("pk").first()
    if owner is None:
        owner = UserModel.objects.create_user(email=PLACEHOLDER_OWNER_EMAIL)  # unusable password
    return owner


def assign_default_owner(app_label, model_name, field_name="user"):
    """RunPython op that fills an empty user FK with the first existing user (or a placeholder one)."""

    def forwards(apps, schema_editor):
        Model = apps.get_model(app_label, model_name)
        orphans = Model.objects.filter(**{f"{field_name}__isnull": True})
        if orphans.exists():
            orphans.update(**{field_name: _get_default_owner(apps)})

        if schema_editor.connection.vendor == "postgresql":
            # Flush deferred FK checks so the following NOT NULL ALTER doesn't hit "pending trigger events".
            schema_editor.execute("SET CONSTRAINTS ALL IMMEDIATE")

    return migrations.RunPython(forwards, migrations.RunPython.noop)
