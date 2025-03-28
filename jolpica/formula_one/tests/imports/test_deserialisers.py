from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from jolpica.formula_one import models as f1
from jolpica.formula_one.importer.deserialisers import (
    BaseDeserializer,
    DriverDeserialiser,
    LapDeserialiser,
    PitStopDeserialiser,
    RoundEntryDeserialiser,
    SessionEntryDeserialiser,
    UnableToParseValueError,
)


@pytest.fixture
def entry_list_data():
    return {
        "object_type": "round_entry",
        "foreign_keys": {"year": 2023, "round": 22},
        "objects": [
            {"car_number": 1, "name": "Max Verstappen", "team": "Oracle Red Bull Racing"},
            {"car_number": 11, "name": "Sergio Perez", "team": "Oracle Red Bull Racing"},
            {"car_number": 16, "name": "Charles Leclerc", "team": "Scuderia Ferrari"},
            {"car_number": 55, "name": "Carlos Sainz", "team": "Scuderia Ferrari"},
            {"car_number": 63, "name": "George Russell", "team": "Mercedes-AMG PETRONAS F1 Team"},
            {"car_number": 44, "name": "Lewis Hamilton", "team": "Mercedes-AMG PETRONAS F1 Team"},
            {"car_number": 31, "name": "Esteban Ocon", "team": "BWT Alpine F1 Team"},
            {"car_number": 10, "name": "Pierre Gasly", "team": "BWT Alpine F1 Team"},
            {"car_number": 81, "name": "Oscar Piastri", "team": "McLaren F1 Team"},
            {"car_number": 4, "name": "Lando Norris", "team": "McLaren F1 Team"},
            {"car_number": 77, "name": "Valtteri Bottas", "team": "Alfa Romeo F1 Team Stake"},
            {"car_number": 24, "name": "Zhou Guanyu", "team": "Alfa Romeo F1 Team Stake"},
            {"car_number": 18, "name": "Lance Stroll", "team": "Aston Martin Aramco Cognizant F1 Team"},
            {"car_number": 14, "name": "Fernando Alonso", "team": "Aston Martin Aramco Cognizant F1 Team"},
            {"car_number": 20, "name": "Kevin Magnussen", "team": "MoneyGram Haas F1 Team"},
            {"car_number": 27, "name": "Nico Hulkenberg", "team": "MoneyGram Haas F1 Team"},
            {"car_number": 3, "name": "Daniel Ricciardo", "team": "Scuderia AlphaTauri"},
            {"car_number": 22, "name": "Yuki Tsunoda", "team": "Scuderia AlphaTauri"},
            {"car_number": 23, "name": "Alexander Albon", "team": "Williams Racing"},
            {"car_number": 2, "name": "Logan Sargeant", "team": "Williams Racing"},
            {"car_number": 39, "name": "Robert Shwartzman", "team": "Scuderia Ferrari"},
            {"car_number": 34, "name": "Felipe Drugovich", "team": "Aston Martin Aramco Cognizant F1 Team"},
            {"car_number": 50, "name": "Oliver Bearman", "team": "MoneyGram Haas F1 Team"},
            {"car_number": 61, "name": "Jack Doohan", "team": "BWT Alpine F1 Team"},
            {"car_number": 29, "name": "Patricio O'Ward", "team": "McLaren F1 Team"},
            {"car_number": 42, "name": "Frederik Vesti", "team": "Mercedes-AMG PETRONAS F1 Team"},
            {"car_number": 36, "name": "Jake Dennis", "team": "Oracle Red Bull Racing"},
            {"car_number": 37, "name": "Isack Hadjar", "team": "Oracle Red Bull Racing"},
            {"car_number": 98, "name": "Theo Pourchaire", "team": "Alfa Romeo F1 Team Stake"},
            {"car_number": 45, "name": "Zak O'Sullivan", "team": "Williams Racing"},
        ],
    }


@pytest.mark.django_db
def test_deserialise_classification(entry_list_data):
    deserialised = DriverDeserialiser().deserialise(entry_list_data)

    assert len(deserialised.models) + len(deserialised.object_failures) == len(entry_list_data["objects"])
    assert len(deserialised.models) == 20
    assert len(deserialised.object_failures) == 10

    new_models = 0
    existing_models = 0
    for model in deserialised.models:
        try:
            f1.RoundEntry.objects.get(round_id=model.round_id, team_driver_id=model.team_driver_id)
        except f1.RoundEntry.DoesNotExist:
            new_models += 1
        else:
            existing_models += 1

    assert new_models == 0
    assert existing_models == len(deserialised.models)


@pytest.mark.parametrize(
    ["year", "round", "driver", "team", "object", "error"],
    [
        (2023, 22, "Max Verstappen", "invalid", {"car_number": 1}, "(unmapped team name)"),
        (2023, 22, "Max Verstappen", "invalid", {"car_number": 1}, "(team miss)"),
        (2023, 22, "Invalid Driver", "Oracle Red Bull Racing", {"car_number": 1}, "(driver miss)"),
        (2009, 1, "Sébastien AMBIGUOUS", "Toro Rosso", {}, "Multiple TeamDrivers found"),
    ],
)
@pytest.mark.django_db
def test_round_entry_deserialiser_get_team_driver_error(year, round, driver, team, object, error):
    data = {
        "object_type": "round_entry",
        "foreign_keys": {
            "year": year,
            "round": round,
            "driver_name": driver,
            "team_name": team,
        },
        "objects": [object],
    }
    deserialiser = RoundEntryDeserialiser()
    result = deserialiser.deserialise(data)

    assert result.has_failure
    assert result.foreign_key_failure
    assert (
        "TeamDriver not found" in result.foreign_key_failure
        or "Multiple TeamDrivers found" in result.foreign_key_failure
    )
    assert error in result.foreign_key_failure


@pytest.fixture
def session_entry_race_data():
    return {
        "object_type": "classification",
        "foreign_keys": {"year": 2023, "round": 18, "session": "R", "car_number": 1},
        "objects": [
            {
                "position": 1,
                "is_classified": True,
                "status": 0,
                "points": 25.0,
                "time": timedelta(seconds=5721, microseconds=362000),
                "laps_completed": 56,
            }
        ],
    }


@pytest.mark.django_db
def test_deserialise_session_entries(session_entry_race_data):
    deserialised = SessionEntryDeserialiser().deserialise(session_entry_race_data)

    assert len(deserialised.models) + len(deserialised.object_failures) == len(session_entry_race_data["objects"])
    assert len(deserialised.models) == 1
    assert len(deserialised.object_failures) == 0

    new_models = 0
    existing_models = 0
    for model in deserialised.models:
        try:
            f1.SessionEntry.objects.get(session_id=model.session_id, round_entry_id=model.round_entry_id)
        except f1.SessionEntry.DoesNotExist:
            new_models += 1
        else:
            existing_models += 1

    assert new_models == 0
    assert existing_models == len(deserialised.models)


@pytest.mark.parametrize(
    ["year", "round", "session", "car_number", "object", "error"],
    [
        (2023, 22, "R", 1, {"invalid_key": "value"}, "Invalid key: invalid_key"),
        (2023, 99, "R", 1, {}, "Session matching query does not exist"),
        (2023, 22, "R", 99, {}, "RoundEntry matching query does not exist"),
    ],
)
@pytest.mark.django_db
def test_session_entry_deserialiser_invalid_data(year, round, session, car_number, object, error):
    data = {
        "object_type": "session_entry",
        "foreign_keys": {"year": year, "round": round, "session": session, "car_number": car_number},
        "objects": [object],
    }
    deserialiser = SessionEntryDeserialiser()
    result = deserialiser.deserialise(data)

    assert result.has_failure
    if result.foreign_key_failure:
        assert error in result.foreign_key_failure
    else:
        assert len(result.object_failures) == 1
        assert error in result.object_failures[0][1]


@pytest.fixture
def lap_data():
    return {
        "object_type": "lap",
        "foreign_keys": {"year": 2023, "round": 18, "session": "R", "car_number": 1},
        "objects": [
            {"number": 1, "position": 1, "time": timedelta(minutes=1, seconds=30), "average_speed": 200.0},
            {"number": 2, "position": 1, "time": timedelta(minutes=1, seconds=29), "average_speed": 201.0},
        ],
    }


@pytest.mark.django_db
def test_deserialise_laps(lap_data):
    deserialised = LapDeserialiser().deserialise(lap_data)

    assert len(deserialised.models) + len(deserialised.object_failures) == len(lap_data["objects"])
    assert len(deserialised.models) == 2
    assert len(deserialised.object_failures) == 0

    new_laps = 0
    existing_laps = 0
    for lap in deserialised.models:
        try:
            f1.Lap.objects.get(session_entry_id=lap.session_entry_id, number=lap.number)
        except f1.Lap.DoesNotExist:
            new_laps += 1
        else:
            existing_laps += 1

    assert new_laps == 0
    assert existing_laps == len(deserialised.models)


@pytest.mark.parametrize(
    ["year", "round", "session", "car_number", "object", "error"],
    [
        (2023, 18, "R", 1, {"invalid_key": "value"}, "Invalid key: invalid_key"),
        (
            2023,
            99,
            "R",
            1,
            {},
            "SessionEntry matching query does not exist",
        ),
    ],
)
@pytest.mark.django_db
def test_lap_deserialiser_invalid_data(year, round, session, car_number, object, error):
    data = {
        "object_type": "lap",
        "foreign_keys": {"year": year, "round": round, "session": session, "car_number": car_number},
        "objects": [object],
    }
    deserialiser = LapDeserialiser()
    result = deserialiser.deserialise(data)

    assert result.has_failure
    if result.object_failures:
        assert len(result.object_failures) == 1
        assert error in result.object_failures[0][1]
    else:
        assert error in result.foreign_key_failure


@pytest.fixture
def pit_stop_data():
    return {
        "object_type": "pit_stop",
        "foreign_keys": {"year": 2023, "round": 18, "session": "R", "car_number": 1, "lap": 1},
        "objects": [
            {"number": 1, "duration": timedelta(seconds=25), "local_timestamp": timedelta(minutes=30)},
            {"number": 2, "duration": timedelta(seconds=24), "local_timestamp": timedelta(minutes=60)},
        ],
    }


@pytest.mark.django_db
def test_deserialise_pit_stops(pit_stop_data):
    deserialised = PitStopDeserialiser().deserialise(pit_stop_data)

    assert len(deserialised.models) + len(deserialised.object_failures) == len(pit_stop_data["objects"])
    assert len(deserialised.models) == 2
    assert len(deserialised.object_failures) == 0

    new_pit_stops = 0
    existing_pit_stops = 0
    for pit_stop in deserialised.models:
        try:
            f1.PitStop.objects.get(session_entry_id=pit_stop.session_entry_id, number=pit_stop.number)
        except f1.PitStop.DoesNotExist:
            new_pit_stops += 1
        else:
            existing_pit_stops += 1

    assert new_pit_stops == 0
    assert existing_pit_stops == len(deserialised.models)


@pytest.mark.parametrize(
    ["year", "round", "session", "car_number", "object", "error"],
    [
        (2023, 18, "R", 1, {"invalid_key": "value"}, "KeyError"),
        (2023, 99, "R", 1, {}, "SessionEntry matching query does not exist"),
    ],
)
@pytest.mark.django_db
def test_pit_stop_deserialiser_invalid_data(year, round, session, car_number, object, error):
    data = {
        "object_type": "pit_stop",
        "foreign_keys": {"year": year, "round": round, "session": session, "car_number": car_number},
        "objects": [object],
    }
    deserialiser = PitStopDeserialiser()
    result = deserialiser.deserialise(data)

    assert result.has_failure
    if result.foreign_key_failure:
        assert error in result.foreign_key_failure
    else:
        assert len(result.object_failures) == 1
        assert error in result.object_failures[0][1]


@pytest.mark.parametrize(
    ["input_data", "expected_output"],
    [
        (
            {"time": {"_type": "timedelta", "days": 1, "hours": 2, "minutes": 30, "seconds": 45}},
            {"time": timedelta(days=1, hours=2, minutes=30, seconds=45)},
        ),
        (
            {"time": {"_type": "timedelta", "milliseconds": 1000}},
            {"time": timedelta(microseconds=1000000)},
        ),
        (
            {"time": {"_type": "timedelta", "milliseconds": 1000}},
            {"time": timedelta(milliseconds=1000)},
        ),
        (
            {"time": {"_type": "timedelta", "seconds": 3600}, "other_field": "value"},
            {"time": timedelta(seconds=3600), "other_field": "value"},
        ),
    ],
)
def test_parse_field_values(input_data, expected_output):
    result = BaseDeserializer.parse_field_values(MagicMock(), input_data)
    assert result == expected_output


@pytest.mark.parametrize(
    ["input_data", "expected_error"],
    [
        (
            {"time": {"_type": "timedelta", "self_destruction_time": 1000}},
            "self_destruction_time is not a valid field for given type",
        ),
    ],
)
def test_error_on_invalid_parse_field_values(input_data, expected_error):
    with pytest.raises(UnableToParseValueError):
        BaseDeserializer.parse_field_values(MagicMock(), input_data)


@pytest.mark.parametrize(
    ["deserializer_class", "foreign_keys", "field_values", "expected_exception", "expected_message"],
    [
        (
            SessionEntryDeserialiser,
            {"session_id": 1, "round_entry_id": 1},
            {
                "position": 1,
                "is_classified": True,
                "status": 0,
                "points": 25.0,
                "time": {"_type": "timedelta", "milliseconds": 1000},
                "laps_completed": 56,
                "invalid_key": "value",
            },
            ValueError,
            "Invalid key: invalid_key",
        ),
        (
            LapDeserialiser,
            {"session_entry_id": 1},
            {
                "number": 1,
                "position": 1,
                "time": timedelta(minutes=1, seconds=30),
                "average_speed": 200.0,
                "invalid_key": "value",
            },
            ValueError,
            "Invalid key: invalid_key",
        ),
        (
            PitStopDeserialiser,
            {"session_entry_id": 1},
            {
                "number": 1,
                "duration": timedelta(seconds=25),
                "local_timestamp": timedelta(minutes=30),
                "invalid_key": "value",
            },
            ValueError,
            "Invalid key: invalid_key",
        ),
    ],
)
def test_create_model_instance_invalid_key(
    deserializer_class, foreign_keys, field_values, expected_exception, expected_message
):
    deserializer = deserializer_class()
    with pytest.raises(expected_exception) as excinfo:
        deserializer.create_model_instance(foreign_keys, field_values)
    assert str(excinfo.value) == expected_message
