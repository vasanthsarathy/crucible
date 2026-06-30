from crucible.reviewer_personas import BUILTIN_PERSONAS, get_active_personas
from crucible.venue_profiles import VENUE_PROFILES, get_venue_weights
from crucible.store import ProjectStore


def test_seven_builtin_personas():
    assert len(BUILTIN_PERSONAS) == 7
    ids = {p.reviewer_id for p in BUILTIN_PERSONAS}
    assert ids == {"flash", "archimedes", "edison", "copernicus", "linnaeus", "orwell", "socrates"}


def test_linnaeus_and_socrates_not_voting():
    non_voting = {p.reviewer_id for p in BUILTIN_PERSONAS if not p.is_voting}
    assert non_voting == {"linnaeus", "socrates"}


def test_voting_reviewers_count():
    voting = [p for p in BUILTIN_PERSONAS if p.is_voting]
    assert len(voting) == 5


def test_venue_profiles_exist():
    expected = {"NeurIPS", "ICLR", "ICML", "ACL", "EMNLP", "Nature", "TMLR", "CVPR", "AAAI"}
    assert expected.issubset(set(VENUE_PROFILES.keys()))


def test_get_active_personas_returns_builtins_plus_custom(tmp_path):
    store = ProjectStore(tmp_path / ".crucible")
    pid = store.create_project("Test", "seed")
    personas = get_active_personas(pid, store)
    assert len(personas) == 7  # builtins only, no custom


def test_get_venue_weights_for_iclr():
    weights = get_venue_weights("ICLR")
    assert weights["archimedes"] > 1.0
    assert weights["edison"] > 1.0
