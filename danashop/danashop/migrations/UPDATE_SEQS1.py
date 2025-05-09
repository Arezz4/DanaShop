from django.db import migrations, connection

def set_sqlite_sequence(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE sqlite_sequence SET seq = 1000 WHERE name = 'users';")
        cursor.execute("UPDATE sqlite_sequence SET seq = 1000 WHERE name = 'products';")
        cursor.execute("UPDATE sqlite_sequence SET seq = 1000 WHERE name = 'shop_category';")

class Migration(migrations.Migration):

    dependencies = [
        ('danashop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_sqlite_sequence),
    ]
