from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0006_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='django_admin_log',
            name='user_id',
            field=models.ForeignKey(to='doctors_user', on_delete=models.CASCADE),
        ),
    ]
