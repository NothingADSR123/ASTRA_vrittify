def calculate_final_score(ai_likelihood: float, handwriting_similarity: float) -> dict:
    """
    Combines AI likelihood and handwriting similarity into a final suspicion score.
    """
    handwriting_suspicion = 1 - handwriting_similarity
    
    # Final score formula
    final_score = (0.6 * ai_likelihood) + (0.3 * handwriting_suspicion) + 0.1
    final_score = max(0.0, min(1.0, float(final_score)))
    
    if final_score < 0.35:
        risk_level = "LOW"
    elif final_score <= 0.65:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
        
    flags = []
    if ai_likelihood > 0.6:
        flags.append("High AI likelihood detected")
    if handwriting_similarity < 0.4:
        flags.append("Significant handwriting deviation")
    
    # These flags are based on the stylometry heuristics indirectly
    # We'll pass more specific flags from the main route if needed
    
    return {
        "suspicion_score": final_score,
        "risk_level": risk_level,
        "flags": flags
    }
