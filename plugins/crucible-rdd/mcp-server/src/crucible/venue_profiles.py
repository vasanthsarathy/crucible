from __future__ import annotations

from .models import VenueProfile

VENUE_PROFILES: dict[str, VenueProfile] = {
    "NeurIPS": VenueProfile(
        venue="NeurIPS",
        reviewer_weights={
            "flash": 1.0,
            "archimedes": 1.2,
            "edison": 1.2,
            "copernicus": 1.3,
            "linnaeus": 1.0,
            "orwell": 1.0,
            "socrates": 1.0,
        },
        notes="Balanced across all dimensions. Copernicus weighted for significance. Strong emphasis on insight conveyed.",
    ),
    "ICLR": VenueProfile(
        venue="ICLR",
        reviewer_weights={
            "flash": 1.0,
            "archimedes": 1.4,
            "edison": 1.4,
            "copernicus": 1.1,
            "linnaeus": 1.0,
            "orwell": 1.0,
            "socrates": 1.1,
        },
        notes="Heaviest emphasis on reproducibility and rigor. Open review culture demands transparency.",
    ),
    "ICML": VenueProfile(
        venue="ICML",
        reviewer_weights={
            "flash": 1.0,
            "archimedes": 1.3,
            "edison": 1.2,
            "copernicus": 1.2,
            "linnaeus": 1.0,
            "orwell": 1.0,
            "socrates": 1.0,
        },
        notes="Strong theory + empirics balance. Clarity valued.",
    ),
    "ACL": VenueProfile(
        venue="ACL",
        reviewer_weights={
            "flash": 1.0,
            "archimedes": 1.0,
            "edison": 1.2,
            "copernicus": 1.1,
            "linnaeus": 1.4,
            "orwell": 1.4,
            "socrates": 1.0,
        },
        notes="Thorough related work and clear writing are paramount. Linguistic insight valued alongside metrics.",
    ),
    "EMNLP": VenueProfile(
        venue="EMNLP",
        reviewer_weights={
            "flash": 1.0,
            "archimedes": 1.0,
            "edison": 1.2,
            "copernicus": 1.1,
            "linnaeus": 1.4,
            "orwell": 1.3,
            "socrates": 1.0,
        },
        notes="Similar to ACL. Reproducibility emphasized.",
    ),
    "CVPR": VenueProfile(
        venue="CVPR",
        reviewer_weights={
            "flash": 1.2,
            "archimedes": 1.0,
            "edison": 1.4,
            "copernicus": 1.1,
            "linnaeus": 1.1,
            "orwell": 1.0,
            "socrates": 1.0,
        },
        notes="Benchmarking rigor critical. Visual quality and comparison completeness emphasized.",
    ),
    "AAAI": VenueProfile(
        venue="AAAI",
        reviewer_weights={
            "flash": 1.0,
            "archimedes": 1.1,
            "edison": 1.1,
            "copernicus": 1.2,
            "linnaeus": 1.2,
            "orwell": 1.1,
            "socrates": 1.0,
        },
        notes="Broad AI scope. Significance and scholarship both weighted.",
    ),
    "Nature": VenueProfile(
        venue="Nature",
        reviewer_weights={
            "flash": 1.2,
            "archimedes": 1.1,
            "edison": 1.2,
            "copernicus": 1.6,
            "linnaeus": 1.2,
            "orwell": 1.3,
            "socrates": 1.1,
        },
        notes="Broad significance required. Copernicus dominant. Orwell critical — Nature requires non-specialist accessibility.",
    ),
    "TMLR": VenueProfile(
        venue="TMLR",
        reviewer_weights={
            "flash": 0.8,
            "archimedes": 1.2,
            "edison": 1.5,
            "copernicus": 1.0,
            "linnaeus": 1.0,
            "orwell": 1.1,
            "socrates": 1.2,
        },
        notes="Reproducibility and transparency paramount. Rolling review. Flash weighted down — TMLR values thorough work over novelty framing.",
    ),
}


def get_venue_weights(venue: str) -> dict[str, float]:
    """Returns reviewer weight multipliers for a venue, or all 1.0 if unknown."""
    if venue in VENUE_PROFILES:
        return VENUE_PROFILES[venue].reviewer_weights
    return {
        r: 1.0
        for r in ["flash", "archimedes", "edison", "copernicus", "linnaeus", "orwell", "socrates"]
    }
