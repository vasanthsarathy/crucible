from crucible.reviewer_personas import BUILTIN_PERSONAS, get_active_personas
from crucible.store import ProjectStore
from crucible.venue_profiles import VENUE_PROFILES, get_venue_weights


def test_nine_builtin_personas():
    assert len(BUILTIN_PERSONAS) == 9
    ids = {p.reviewer_id for p in BUILTIN_PERSONAS}
    assert ids == {
        "flash",
        "archimedes",
        "edison",
        "copernicus",
        "linnaeus",
        "orwell",
        "socrates",
        "cicero",
        "rawls",
    }


def test_voting_reviewers_count():
    voting = [p for p in BUILTIN_PERSONAS if p.is_voting]
    assert len(voting) == 5  # flash, archimedes, edison, copernicus, orwell


def test_non_voting_personas():
    non_voting = {p.reviewer_id for p in BUILTIN_PERSONAS if not p.is_voting}
    assert non_voting == {"linnaeus", "socrates", "cicero", "rawls"}


def test_champion_and_ethics_roles():
    by_id = {p.reviewer_id: p for p in BUILTIN_PERSONAS}
    assert by_id["cicero"].role == "champion"
    assert by_id["rawls"].role == "ethics"
    assert not by_id["cicero"].is_voting
    assert not by_id["rawls"].is_voting


def test_venue_profiles_exist():
    expected = {"NeurIPS", "ICLR", "ICML", "ACL", "EMNLP", "Nature", "TMLR", "CVPR", "AAAI"}
    assert expected.issubset(set(VENUE_PROFILES.keys()))


def test_get_active_personas_returns_nine(tmp_path):
    store = ProjectStore(tmp_path / ".crucible")
    pid = store.create_project("Test", "seed")
    personas = get_active_personas(pid, store)
    assert len(personas) == 9


def test_get_venue_weights_for_iclr():
    weights = get_venue_weights("ICLR")
    assert weights["archimedes"] > 1.0
    assert weights["edison"] > 1.0


def test_no_persona_rejects_by_default():
    for p in BUILTIN_PERSONAS:
        # "not grounds for rejection" is a disclaimer, not a rejection stance.
        stance = p.default_stance.lower().replace("not grounds for rejection", "")
        assert "reject" not in stance, p.reviewer_id


def test_every_persona_has_excellence_and_axis():
    for p in BUILTIN_PERSONAS:
        assert p.excellence_signal, p.reviewer_id
        assert p.axis in {"soundness", "significance", "cross_cutting"}


def test_socrates_is_intellectual_honesty():
    socrates = next(p for p in BUILTIN_PERSONAS if p.reviewer_id == "socrates")
    assert "honest" in socrates.lens.lower() or "honest" in socrates.evaluation_focus.lower()


def test_venue_notes_mention_axes():
    # Notes should reflect the soundness/significance framing, not the old vote language.
    acl = VENUE_PROFILES["ACL"].notes.lower()
    assert "soundness" in acl and "excitement" in acl
