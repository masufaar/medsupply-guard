import re

def is_clinical_question(text: str) -> bool:
    """
    Detects if the input text contains terms that request clinical advice,
    diagnosis, or prescribing information.
    """
    if not text:
        return False
        
    clinical_terms = [
        r"\bdiagnose\b",
        r"\bdiagnosis\b",
        r"\bprescribe\b",
        r"\bprescription\b",
        r"\bdosage\b",
        r"\bdose\b",
        r"\bsubstitute treatment\b",
        r"\bpatient treatment\b",
        r"\bside effects\b",
        r"\bcontraindication\b",
        r"\bcontraindications\b",
        r"\bsymptoms\b",
        r"\bcure\b",
        r"\btreat\b"
    ]
    
    pattern = re.compile("|".join(clinical_terms), re.IGNORECASE)
    return bool(pattern.search(text))
