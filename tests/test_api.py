# Built-ins

# Project
from pobapi import api
from pobapi import config
from pobapi import models
from pobapi import stats

# Third-party
import pytest

BASE_URL = "https://www.pathofexile.com/passive-skill-tree/"


@pytest.fixture(scope="module")
def build():
    with open("../data/test_code.txt") as f:
        code = f.read()
    return api.from_import_code(code)


def _assert_group(skill_group, test_list):
    for g, t in zip(skill_group, test_list):
        assert g.name == t[0]
        assert g.enabled == t[1]
        assert g.level == t[2]
        if isinstance(g, models.Gem):
            assert g.quality == t[3]


def test_class_name(build):
    assert build.class_name == "Scion"


def test_ascendancy_name(build):
    assert build.ascendancy_name == "Ascendant"


def test_level(build):
    assert build.level == 1


def test_bandit(build):
    assert build.bandit == "Alira"


def test_notes(build):
    assert build.notes == "Test string."


def test_second_weapon_set(build):
    assert build.second_weapon_set is True


def test_stats(build):
    assert isinstance(build.stats, stats.Stats)
    assert build.stats.life == 163
    assert build.stats.mana == 60


def test_config(build):
    assert isinstance(build.config, config.Config)
    assert build.config.enemy_boss == "Shaper"


def test_active_item_set(build):
    assert build.active_item_set.body_armour == 1


def test_item_sets(build):
    for item_set in build.item_sets:
        assert item_set.body_armour == 1


def test_active_skill_group(build):
    assert build.active_skill_group.enabled is True
    assert build.active_skill_group.label == "Test label."
    assert build.active_skill_group.active == 1
    test_list = [
        ("Arc", True, 20, 1),
        ("Curse On Hit", True, 20, 2),
        ("Conductivity", True, 20, 3),
    ]
    _assert_group(build.active_skill_group.abilities, test_list)


def test_skill_groups(build):
    skill_group = build.skill_groups[0]
    assert skill_group.enabled is True
    assert skill_group.label == "Test label."
    assert skill_group.active == 1
    test_list = [
        ("Arc", True, 20, 1),
        ("Curse On Hit", True, 20, 2),
        ("Conductivity", True, 20, 3),
    ]
    _assert_group(skill_group.abilities, test_list)

    skill_group = build.skill_groups[1]
    assert skill_group.enabled is True
    assert skill_group.label == ""
    assert skill_group.active == 1
    test_list = [
        ("Herald of Ash", True, 20, 0),
        ("Herald of Ice", True, 20, 0),
        ("Herald of Thunder", True, 20, 0),
    ]
    _assert_group(skill_group.abilities, test_list)

    skill_group = build.skill_groups[2]
    assert skill_group.enabled is True
    assert skill_group.label == ""
    assert skill_group.active == 1
    test_list = [
        ("Abberath's Fury", True, 7),
        ("Added Cold Damage", True, 20, 0),
        ("Added Lightning Damage", True, 20, 0),
        ("Hypothermia", True, 20, 0),
        ("Concentrated Effect", True, 20, 0),
    ]
    _assert_group(skill_group.abilities, test_list)


def test_skill_gems(build):
    test_list_active = [
        ("Arc", True, 20, 1),
        ("Curse On Hit", True, 20, 2),
        ("Conductivity", True, 20, 3),
    ]
    test_list_passive = [
        ("Herald of Ash", True, 20, 0),
        ("Herald of Ice", True, 20, 0),
        ("Herald of Thunder", True, 20, 0),
        ("Added Cold Damage", True, 20, 0),
        ("Added Lightning Damage", True, 20, 0),
        ("Hypothermia", True, 20, 0),
        ("Concentrated Effect", True, 20, 0),
    ]
    _assert_group(build.skill_gems, test_list_active + test_list_passive)


def test_active_skill(build):
    test_list = [("Arc", True, 20, 1)]
    _assert_group([build.active_skill], test_list)


def test_active_skill_tree(build):
    assert (
        build.active_skill_tree.url == BASE_URL + "AAAABAABAJitGFbaYij62E1odILHlKD56A=="
    )
    # fmt: off
    assert build.active_skill_tree.nodes == \
        [39085, 6230, 55906, 10490, 55373, 26740, 33479, 38048, 63976]
    # fmt: on
    assert build.active_skill_tree.sockets == {}


def test_trees(build):
    for tree in build.trees:
        assert tree.url == BASE_URL + "AAAABAABAJitGFbaYij62E1odILHlKD56A=="
        # fmt: off
        assert tree.nodes == \
            [39085, 6230, 55906, 10490, 55373, 26740, 33479, 38048, 63976]
        # fmt: on
        assert tree.sockets == {}


def test_keystones(build):
    assert 39085 in build.active_skill_tree.nodes  # 39085: Elemental Equilibrium


def test_items(build):
    for i in build.items:
        if i.name == "Inpulsa's Broken Heart":
            assert i.rarity == "Unique"
            assert i.name == "Inpulsa's Broken Heart"
            assert i.base == "Sadist Garb"
            assert i.shaper is True
            assert i.elder is False
            assert i.quality == 20
            assert i.sockets == (("R", "G", "B"), ("B", "B", "B"))
            assert i.level_req == 68
            assert i.item_level == 1
            assert i.implicit == 2
            assert (
                i.text
                == """45% increased Damage
5% increased maximum Life
+70 to maximum Life
35% increased Damage if you have Shocked an Enemy Recently
33% increased Effect of Shock
Unaffected by Shock
Shocked Enemies you Kill Explode, dealing 5% of
their Maximum Life as Lightning Damage which cannot Shock
Corrupted"""
            )
