import re
import yaml
from typing import Dict, List, Set
from pathlib import Path

def load_mapping(path: Path) -> Dict[str, Set[str]]:
    """
    Load the research interests mapping from YAML file.
    """
    mapping_file = path
    with open(mapping_file, 'r', encoding='utf-8') as f:
        yaml_mapping = yaml.safe_load(f)
    
    # Convert lists to sets for faster lookups
    return {k: set(v) for k, v in yaml_mapping.items()}

def normalize_string(s: str) -> str:
    """
    Normalize a string by converting to lowercase and removing special characters.
    """
    # Convert to lowercase
    s = s.lower()
    # Remove special characters and extra whitespace
    s = re.sub(r'[^\w\s]', ' ', s)
    # Remove extra whitespace
    s = ' '.join(s.split())
    return s

def get_canonical_term(term: str, mapping: Dict[str, Set[str]]) -> str:
    """
    Get the canonical term for a given research interest.
    """
    normalized_term = normalize_string(term)
    
    # First check if the normalized term matches any canonical term directly
    if normalized_term in mapping:
        return normalized_term
    
    # Then check if it matches any variant
    for canonical, variants in mapping.items():
        normalized_variants = {normalize_string(v) for v in variants}
        if normalized_term in normalized_variants:
            return canonical
    
    # If no mapping found, return the normalized term
    return normalized_term

def normalize_interests(interests: List[str], mapping: Dict[str, Set[str]]) -> List[str]:
    """
    Normalize a list of research interests.
    
    Args:
        interests: List of research interest strings
        
    Returns:
        List of normalized, canonical research interests
    """
    # Get canonical terms and remove duplicates
    normalized = {get_canonical_term(interest, mapping) for interest in interests}
    return sorted(list(normalized))

def analyze_unique_terms(interests: List[str]) -> Dict[str, Set[str]]:
    """
    Analyze which terms are not in our mapping and could be added.
    
    Args:
        interests: List of all research interests
        
    Returns:
        Dictionary mapping normalized terms to their original variations
    """
    unmapped = {}
    for interest in interests:
        normalized = normalize_string(interest)
        canonical = get_canonical_term(interest)
        if normalized != normalize_string(canonical):
            if canonical not in unmapped:
                unmapped[canonical] = set()
            unmapped[canonical].add(interest)
    return unmapped

if __name__ == "__main__":
    # Example usage
    test_interests = [
        "machine learning",
        "ML",
        "deep learning",
        "Deep Learning",
        "physics-informed machine learning",
        "physics-​informed machine learning",
        "3d scene understanding",
        "scene understanding",
        "optimization",
        "optimisation"
    ]
    
    normalized = normalize_interests(test_interests)
    print("Normalized interests:", normalized)
    
    # Analyze unmapped terms
    unmapped = analyze_unique_terms(test_interests)
    print("\nUnmapped terms:", unmapped) 