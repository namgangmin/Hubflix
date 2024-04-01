# Generated by Django 5.0.3 on 2024-04-01 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contents",
            fields=[
                (
                    "contents_id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("_type", models.CharField(max_length=10)),
                ("title", models.CharField(max_length=100)),
                ("genre", models.CharField(max_length=100)),
                ("production_countries", models.CharField(max_length=200)),
                ("seasons_number", models.IntegerField(blank=True, null=True)),
                ("release_date", models.DateField(blank=True, null=True)),
                ("summary", models.CharField(blank=True, max_length=300, null=True)),
                ("have_ott", models.IntegerField(blank=True, null=True)),
                ("runtime", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "contents",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Have_ott",
            fields=[
                (
                    "have_ott_num",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
            ],
            options={
                "db_table": "have_ott",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Ott",
            fields=[
                (
                    "ott_name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                (
                    "ott_icon",
                    models.ImageField(
                        blank=True, null=True, upload_to="uploads/%Y/%m/%d/"
                    ),
                ),
            ],
            options={
                "db_table": "ott",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("post_id", models.IntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=45)),
                ("contents", models.CharField(max_length=200)),
                ("time", models.DateField(blank=True, null=True)),
            ],
            options={
                "db_table": "post",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("review_num", models.IntegerField(primary_key=True, serialize=False)),
                ("rating", models.IntegerField(blank=True, null=True)),
                ("review_contents", models.CharField(max_length=200)),
                ("review_time", models.DateField()),
            ],
            options={
                "db_table": "review",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="User_link_info",
            fields=[
                (
                    "user_link_num",
                    models.CharField(max_length=200, primary_key=True, serialize=False),
                ),
                ("ott_id", models.CharField(max_length=50)),
                ("ott_password", models.CharField(max_length=100)),
                ("ott_profile", models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                "db_table": "User_link_info",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "user_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("password", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=20)),
                ("phone_number", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=50)),
                ("nickname", models.CharField(max_length=30)),
                ("gender", models.IntegerField()),
                ("birth", models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                "db_table": "users",
                "managed": False,
            },
        ),
    ]
