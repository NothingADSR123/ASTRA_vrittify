import numpy as np
import re

def compute_stylometry(text: str) -> dict:
    """
    Computes stylometry heuristics: burstiness and repetition.
    """
    if not text or len(text.strip()) == 0:
        return {
            "ai_likelihood": 0.0,
            "burstiness": 0.0,
            "repetition_score": 0.0
        }

    # Split into sentences using simple regex
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Check if we have enough text to analyze
    words = re.findall(r'\w+', text.lower())
    if len(words) < 50 or len(sentences) < 3:
        return {
            "ai_likelihood": 0.0,
            "burstiness": 0.0,
            "repetition_score": 0.0
        }

    # Sentence lengths in words
    sentence_lengths = [len(s.split()) for s in sentences]
    mean_length = np.mean(sentence_lengths)
    std_dev = np.std(sentence_lengths)
    
    # Burstiness: High burstiness (high std dev relative to mean) is more human-like.
    # AI tends to have more uniform sentence lengths (low burstiness).
    burstiness = std_dev / mean_length if mean_length > 0 else 0
    
    # Repetition score: ratio of repeated words
    if not words:
        repetition_score = 0
    else:
        unique_words = set(words)
        repetition_score = (len(words) - len(unique_words)) / len(words)

    # AI Likelihood Formula (heuristic)
    # 1 - burstiness: higher score if sentence lengths are uniform
    # repetition * 0.04: slight boost if repetition is high
    ai_score = (1 - min(burstiness, 1.0)) + (repetition_score * 0.04)
    ai_score = max(0.0, min(1.0, float(ai_score)))

    return {
        "ai_likelihood": ai_score,
        "burstiness": float(burstiness),
        "repetition_score": float(repetition_score)
    }
