from django.db import migrations

from api.models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ, SPEECH2TEXT, IMAGE_CLASSIFICATION


def fill_task_type(apps, schema_editor):
    AutoLabelingConfig = apps.get_model('auto_labeling', 'AutoLabelingConfig')
    for config in AutoLabelingConfig.objects.all():
        project = config.project
        if project.project_type in [
            DOCUMENT_CLASSIFICATION,
            IMAGE_CLASSIFICATION,
        ] or project.project_type not in [
            SEQ2SEQ,
            SPEECH2TEXT,
            SEQUENCE_LABELING,
        ]:
            config.task_type = 'Category'
        elif project.project_type in [SEQ2SEQ, SPEECH2TEXT]:
            config.task_type = 'Text'
        else:
            config.task_type = 'Span'
        config.save()


class Migration(migrations.Migration):

    dependencies = [
        ('auto_labeling', '0002_autolabelingconfig_task_type'),
    ]

    operations = [
        migrations.RunPython(
            code=fill_task_type,
            reverse_code=migrations.RunPython.noop
        )
    ]
