#!/usr/bin/env python3
"""
Phase F: Persona Sample Tests
Tests the actual persona pack samples.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from l5.persona_loader import load_persona


PERSONAS = [
    'izzara_friendly_consultant.v1',
    'zeyti_bbnu_creator.v1',
    'tawfiq_sales_closer.v1',
    'jordan_cfo_analyst.v1',
    'raya_campaign_storyteller.v1'
]


def test_all_personas_valid():
    """Test all 5 personas pass schema validation."""
    print("Test 1: All personas pass schema validation")
    
    for persona_id in PERSONAS:
        persona = load_persona(persona_id)
        assert persona is not None
    
    print(f"  ✓ All {len(PERSONAS)} personas valid")


def test_no_vertical_logic():
    """Test no persona includes vertical/industry logic."""
    print("\nTest 2: No vertical/industry logic in personas")
    
    forbidden_keys = ['vertical', 'workflows', 'entities', 'skills']
    
    for persona_id in PERSONAS:
        persona = load_persona(persona_id)
        
        # Check top-level keys only (not nested values like rubric_targets.compliance)
        for key in forbidden_keys:
            assert key not in persona, f"{persona_id} contains forbidden key: {key}"
    
    print("  ✓ No vertical logic found")


def test_rubric_targets_valid():
    """Test all rubric targets have scores 1-5."""
    print("\nTest 3: Rubric targets have valid scores")
    
    for persona_id in PERSONAS:
        persona = load_persona(persona_id)
        rubric = persona['rubric_targets']
        
        for metric, score in rubric.items():
            assert 1 <= score <= 5, f"{persona_id} has invalid {metric} score: {score}"
    
    print("  ✓ All rubric scores valid (1-5)")


def test_language_profiles_differ():
    """Test language and tone settings differ between personas."""
    print("\nTest 4: Language profiles differ meaningfully")
    
    profiles = {}
    for persona_id in PERSONAS:
        persona = load_persona(persona_id)
        lang = persona['language_profile']
        tone = persona['tone']
        
        profile_key = (
            lang['english_ratio'],
            lang['bbnu_ratio'],
            tone['primary_tone'],
            tone['formality_level']
        )
        
        assert profile_key not in profiles, f"Duplicate profile found for {persona_id}"
        profiles[profile_key] = persona_id
    
    print(f"  ✓ All {len(PERSONAS)} personas have unique profiles")


def test_specific_personas():
    """Test specific persona characteristics."""
    print("\nTest 5: Specific persona characteristics")
    
    # Izzara should be friendly and balanced
    izzara = load_persona('izzara_friendly_consultant.v1')
    assert izzara['tone']['primary_tone'] == 'friendly'
    assert izzara['tone']['empathy_level'] >= 4
    
    # Zeyti should be high BBNU
    zeyti = load_persona('zeyti_bbnu_creator.v1')
    assert zeyti['language_profile']['bbnu_ratio'] >= 60
    
    # Tawfiq should be high persuasion
    tawfiq = load_persona('tawfiq_sales_closer.v1')
    assert tawfiq['persuasion']['persuasion_level'] >= 4
    
    # Jordan should be analytical and formal
    jordan = load_persona('jordan_cfo_analyst.v1')
    assert jordan['tone']['primary_tone'] == 'analytical'
    assert jordan['tone']['formality_level'] >= 4
    
    # Raya should be empathetic storyteller
    raya = load_persona('raya_campaign_storyteller.v1')
    assert raya['tone']['primary_tone'] == 'empathetic'
    assert raya['tone']['empathy_level'] >= 4
    
    print("  ✓ Persona characteristics validated")


def main():
    """Run all tests."""
    print("=== Testing Persona Samples ===\n")
    
    tests = [
        test_all_personas_valid,
        test_no_vertical_logic,
        test_rubric_targets_valid,
        test_language_profiles_differ,
        test_specific_personas
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print("\n=== Sample Tests Complete ===\n")
    if failed == 0:
        print(f"✅ PASS: All {passed} tests passed")
        return 0
    else:
        print(f"❌ FAIL: {passed} passed, {failed} failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
