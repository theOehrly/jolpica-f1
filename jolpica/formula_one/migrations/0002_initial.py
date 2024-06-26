# Generated by Django 4.2.6 on 2023-12-03 12:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("formula_one", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseTeam",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Circuit",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "reference",
                    models.CharField(blank=True, max_length=32, null=True, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("locality", models.CharField(blank=True, max_length=255, null=True)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, geography=True, null=True, srid=4326
                    ),
                ),
                ("altitude", models.FloatField(blank=True, null=True)),
                ("wikipedia", models.URLField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Driver",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "reference",
                    models.CharField(blank=True, max_length=32, null=True, unique=True),
                ),
                ("forename", models.CharField(max_length=255)),
                ("surname", models.CharField(max_length=255)),
                (
                    "abbreviation",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "nationality",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "permanent_car_number",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("wikipedia", models.URLField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Lap",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("number", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("position", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("time", models.DurationField(blank=True, null=True)),
                ("average_speed", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Penalty",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "license_points",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("position", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("time", models.DurationField(blank=True, null=True)),
                ("is_time_served_in_pit", models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PitStop",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("number", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("duration", models.DurationField(blank=True, null=True)),
                (
                    "local_timestamp",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PointScheme",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "reference",
                    models.CharField(blank=True, max_length=32, null=True, unique=True),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "driver",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "No Points Awarded"),
                            (1, "1950 - Top 5 get upto 8 points"),
                            (2, "1960 - Top 6 get upto 8 points"),
                            (3, "1961 - Top 6 get upto 9 points"),
                            (5, "1991 - Top 6 get upto 10 points"),
                            (6, "2003 - Top 8 get upto 10 points"),
                            (7, "2010 - Top 10 get upto 25 points"),
                            (21, "Sprint 2021 - Top 3 get upto 3 points"),
                            (22, "Sprint 2022 - Top 8 get upto 8 points"),
                        ]
                    ),
                ),
                (
                    "team",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "No Points Awarded"),
                            (1, "1950 - Top 5 get upto 8 points"),
                            (2, "1960 - Top 6 get upto 8 points"),
                            (3, "1961 - Top 6 get upto 9 points"),
                            (5, "1991 - Top 6 get upto 10 points"),
                            (6, "2003 - Top 8 get upto 10 points"),
                            (7, "2010 - Top 10 get upto 25 points"),
                            (21, "Sprint 2021 - Top 3 get upto 3 points"),
                            (22, "Sprint 2022 - Top 8 get upto 8 points"),
                        ]
                    ),
                ),
                (
                    "fastest_lap",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "No Fastest Lap Point"),
                            (1, "Point for Fastest Lap"),
                            (2, "Point divided between all who got fastest lap"),
                            (3, "Point if in top 10"),
                            (4, "Point if top 10, and >50% race distance"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "team_fastest_lap",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "No Fastest Lap Point"),
                            (1, "Point for Fastest Lap"),
                            (2, "Point divided between all who got fastest lap"),
                            (3, "Point if in top 10"),
                            (4, "Point if top 10, and >50% race distance"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "partial",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "No Partial Points"),
                            (1, "Half Points between 30% - 60%"),
                            (2, "Half Points between 2 Laps - 75%"),
                            (
                                3,
                                "Red Flag Finish, 1-4 Quarters (rounded) of points, minimum 2 laps.",
                            ),
                            (4, "1-4 Quarters (rounded) of points, minimum 2 laps"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "shared_drive",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "No Points"),
                            (1, "Points Shared Equally"),
                            (
                                2,
                                "Shared Points of all drives, unless insufficent distance",
                            ),
                            (3, "Shared Points of highest finish"),
                        ],
                        default=0,
                    ),
                ),
                ("is_double_points", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Race",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("round", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "race_number",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("wikipedia", models.URLField(blank=True, null=True)),
                ("is_cancelled", models.BooleanField(default=False)),
                (
                    "circuit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="races",
                        to="formula_one.circuit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RaceEntry",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("car_number", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="race_entries",
                        to="formula_one.race",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Season",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("year", models.SmallIntegerField(unique=True)),
                ("wikipedia", models.URLField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("R", "Race"),
                            ("Q1", "Qualifying One"),
                            ("Q2", "Qualifying Two"),
                            ("Q3", "Qualifying Three"),
                            ("QA", "Qualifying Avg"),
                            ("QO", "Qualifying Order"),
                            ("QB", "Qualifying Best"),
                            ("FP1", "Practice One"),
                            ("FP2", "Practice Two"),
                            ("FP3", "Practice Three"),
                            ("PQ", "Prequalifying"),
                            ("SR", "Sprint Race"),
                            ("SQ1", "Sprint Qualifying1"),
                            ("SQ2", "Sprint Qualifying2"),
                            ("SQ3", "Sprint Qualifying3"),
                        ],
                        max_length=3,
                    ),
                ),
                ("date", models.DateField(blank=True, null=True)),
                ("time", models.TimeField(blank=True, null=True)),
                (
                    "scheduled_laps",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                ("is_cancelled", models.BooleanField(default=False)),
                (
                    "point_scheme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sessions",
                        to="formula_one.pointscheme",
                    ),
                ),
                (
                    "race",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="formula_one.race",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "reference",
                    models.CharField(blank=True, max_length=32, null=True, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "nationality",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("wikipedia", models.URLField(blank=True, max_length=255, null=True)),
                (
                    "base_team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="teams",
                        to="formula_one.baseteam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamDriver",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "role",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[(0, "Permanent"), (1, "Reserve"), (2, "Junior")],
                        null=True,
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_drivers",
                        to="formula_one.driver",
                    ),
                ),
                (
                    "season",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_drivers",
                        to="formula_one.season",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_drivers",
                        to="formula_one.team",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="team",
            name="drivers",
            field=models.ManyToManyField(
                related_name="teams",
                through="formula_one.TeamDriver",
                to="formula_one.driver",
            ),
        ),
        migrations.CreateModel(
            name="SessionEntry",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("position", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("is_classified", models.BooleanField(blank=True, null=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (0, "Finished"),
                            (1, "Car Finished Lap(s) behind Leader"),
                            (10, "Accident, Collision or Driver Error on Track"),
                            (11, "Mechanial, Safety or Other Retirement"),
                            (20, "Disqualified"),
                            (30, "Withdrawn or Did Not Start"),
                            (40, "Did Not Qualify"),
                            (41, "Did Not Prequalify"),
                        ],
                        null=True,
                    ),
                ),
                ("detail", models.CharField(blank=True, max_length=255, null=True)),
                ("points", models.FloatField(blank=True, null=True)),
                ("grid", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("time", models.DurationField(blank=True, null=True)),
                (
                    "fastest_lap_rank",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "laps_completed",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "fastest_lap",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="formula_one.lap",
                    ),
                ),
                (
                    "race_entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_entries",
                        to="formula_one.raceentry",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_entries",
                        to="formula_one.session",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="session",
            name="race_entries",
            field=models.ManyToManyField(
                related_name="sessions",
                through="formula_one.SessionEntry",
                to="formula_one.raceentry",
            ),
        ),
        migrations.AddField(
            model_name="season",
            name="drivers",
            field=models.ManyToManyField(
                related_name="seasons",
                through="formula_one.TeamDriver",
                to="formula_one.driver",
            ),
        ),
        migrations.AddField(
            model_name="season",
            name="teams",
            field=models.ManyToManyField(
                related_name="seasons",
                through="formula_one.TeamDriver",
                to="formula_one.team",
            ),
        ),
        migrations.AddField(
            model_name="raceentry",
            name="team_driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="race_entries",
                to="formula_one.teamdriver",
            ),
        ),
        migrations.AddField(
            model_name="race",
            name="season",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="races",
                to="formula_one.season",
            ),
        ),
        migrations.AddField(
            model_name="race",
            name="team_drivers",
            field=models.ManyToManyField(
                related_name="races",
                through="formula_one.RaceEntry",
                to="formula_one.teamdriver",
            ),
        ),
        migrations.AddConstraint(
            model_name="pointscheme",
            constraint=models.UniqueConstraint(
                fields=(
                    "driver",
                    "team",
                    "fastest_lap",
                    "team_fastest_lap",
                    "partial",
                    "shared_drive",
                    "is_double_points",
                ),
                name="point_scheme_unique",
            ),
        ),
        migrations.AddField(
            model_name="pitstop",
            name="lap",
            field=models.OneToOneField(
                blank=True,
                limit_choices_to=models.Q(("session_entry", models.F("session_entry"))),
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pit_stop",
                to="formula_one.lap",
            ),
        ),
        migrations.AddField(
            model_name="pitstop",
            name="session_entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pit_stops",
                to="formula_one.sessionentry",
            ),
        ),
        migrations.AddField(
            model_name="penalty",
            name="earned",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="penalties",
                to="formula_one.sessionentry",
            ),
        ),
        migrations.AddField(
            model_name="penalty",
            name="served",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="served_penalties",
                to="formula_one.sessionentry",
            ),
        ),
        migrations.AddField(
            model_name="lap",
            name="session_entry",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="laps",
                to="formula_one.sessionentry",
            ),
        ),
        migrations.AddConstraint(
            model_name="teamdriver",
            constraint=models.UniqueConstraint(
                fields=("team", "driver", "season"), name="team_driver_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="sessionentry",
            constraint=models.UniqueConstraint(
                fields=("session", "race_entry"),
                name="session_entry_unique_session_race_entry",
            ),
        ),
        migrations.AddConstraint(
            model_name="raceentry",
            constraint=models.UniqueConstraint(
                fields=("race", "team_driver", "car_number"), name="race_entry_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="race",
            constraint=models.UniqueConstraint(
                fields=("season", "round"), name="race_unique_season_round"
            ),
        ),
        migrations.AddConstraint(
            model_name="pitstop",
            constraint=models.UniqueConstraint(
                fields=("session_entry", "lap"),
                name="pit_stop_unique_session_entry_lap",
            ),
        ),
        migrations.AddConstraint(
            model_name="pitstop",
            constraint=models.UniqueConstraint(
                fields=("session_entry", "number"),
                name="pit_stop_unique_session_entry_number",
            ),
        ),
        migrations.AddConstraint(
            model_name="lap",
            constraint=models.UniqueConstraint(
                fields=("session_entry", "number"),
                name="lap_unique_session_entry_number",
            ),
        ),
    ]
