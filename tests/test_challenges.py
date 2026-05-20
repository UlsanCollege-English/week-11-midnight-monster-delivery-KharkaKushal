"""Public tests for Week 11: Midnight Monster Delivery."""

from math import inf

import pytest

from src.challenges import (
    HAUNTED_CITY,
    monster_delivery_costs,
    shortest_monster_delivery,
    validate_haunted_map,
)


def test_validate_haunted_map_accepts_valid_graph():
    validate_haunted_map(HAUNTED_CITY)


def test_validate_haunted_map_rejects_negative_weight():
    graph = {
        "Crypt Kitchen": {"Fog Alley": -2},
        "Fog Alley": {},
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_validate_haunted_map_rejects_zero_weight():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 0},
        "Fog Alley": {},
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_validate_haunted_map_rejects_missing_neighbor_node():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_monster_delivery_costs_from_crypt_kitchen():
    result = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")

    assert result["Crypt Kitchen"] == 0
    assert result["Fog Alley"] == 2
    assert result["Bone Bridge"] == 5
    assert result["Moon Bridge"] == 3
    assert result["Goblin Market"] == 6
    assert result["Werewolf Den"] == 8
    assert result["Vampire Tower"] == 10


def test_monster_delivery_costs_keeps_unreachable_as_inf():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
        "Fog Alley": {},
        "Ghost Island": {},
    }

    result = monster_delivery_costs(graph, "Crypt Kitchen")

    assert result["Crypt Kitchen"] == 0
    assert result["Fog Alley"] == 2
    assert result["Ghost Island"] == inf


def test_monster_delivery_costs_missing_start_raises_value_error():
    with pytest.raises(ValueError):
        monster_delivery_costs(HAUNTED_CITY, "Missing Coffin Shop")


def test_shortest_monster_delivery_finds_expected_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 10
    assert path == [
        "Crypt Kitchen",
        "Fog Alley",
        "Moon Bridge",
        "Werewolf Den",
        "Vampire Tower",
    ]


def test_shortest_monster_delivery_start_equals_target():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Crypt Kitchen",
        "Crypt Kitchen",
    )

    assert cost == 0
    assert path == ["Crypt Kitchen"]


def test_shortest_monster_delivery_unreachable_target():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
        "Fog Alley": {},
        "Ghost Island": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Ghost Island",
    )

    assert cost == inf
    assert path == []


def test_shortest_monster_delivery_missing_start_returns_inf_and_empty_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Missing Coffin Shop",
        "Vampire Tower",
    )

    assert cost == inf
    assert path == []


def test_shortest_monster_delivery_missing_target_returns_inf_and_empty_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Crypt Kitchen",
        "Missing Coffin Shop",
    )

    assert cost == inf
    assert path == []


def test_shortest_monster_delivery_handles_cycle():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
        "Fog Alley": {"Crypt Kitchen": 2, "Vampire Tower": 5},
        "Vampire Tower": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 7
    assert path == ["Crypt Kitchen", "Fog Alley", "Vampire Tower"]


def test_shortest_monster_delivery_accepts_either_tied_shortest_path():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2, "Bone Bridge": 2},
        "Fog Alley": {"Vampire Tower": 3},
        "Bone Bridge": {"Vampire Tower": 3},
        "Vampire Tower": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 5
    assert path in [
        ["Crypt Kitchen", "Fog Alley", "Vampire Tower"],
        ["Crypt Kitchen", "Bone Bridge", "Vampire Tower"],
    ]
