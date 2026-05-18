def calculate_final_score(ai_likelihood: float, handwriting_similarity: float, has_stylometry_data: bool = True) -> dict:
    """
    Combines AI likelihood and handwriting similarity into a final suspicion score.
    """
    handwriting_suspicion = 1 - handwriting_similarity
    
    if has_stylometry_data:
        # Full scoring with both stylometry and handwriting
        final_score = (0.6 * ai_likelihood) + (0.3 * handwriting_suspicion) + 0.1
    else:
        # Only use handwriting similarity if we don't have enough text for stylometry
        final_score = 0.5 * handwriting_suspicion + 0.25
    
    final_score = max(0.0, min(1.0, float(final_score)))
    
    if final_score < 0.35:
        risk_level = "LOW"
    elif final_score <= 0.65:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
        
    flags = []
    if has_stylometry_data and ai_likelihood > 0.6:
        flags.append("High AI likelihood detected")
    if handwriting_similarity < 0.4:
        flags.append("Significant handwriting deviation")
    if not has_stylometry_data:
        flags.append("Insufficient text for stylometry analysis")
    
    return {
        "suspicion_score": final_score,
        "risk_level": risk_level,
        "flags": flags
    }
