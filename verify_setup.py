import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

def test_stylometry():
    print("Testing Stylometry Module...")
    from services.stylometry import compute_stylometry
    
    ai_text = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."
    human_text = "I went to the store today. It was quite busy, but I managed to get everything I needed. The weather was lovely as well!"
    
    ai_metrics = compute_stylometry(ai_text)
    human_metrics = compute_stylometry(human_text)
    
    print(f"AI-like Text Metrics: {ai_metrics}")
    print(f"Human-like Text Metrics: {human_metrics}")
    
    assert ai_metrics['ai_likelihood'] > human_metrics['ai_likelihood']
    print("Stylometry test passed!")

def test_scoring():
    print("\nTesting Scoring Module...")
    from services.scoring import calculate_final_score
    
    score_high = calculate_final_score(0.8, 0.2)
    score_low = calculate_final_score(0.2, 0.9)
    
    print(f"High Suspicion Result: {score_high}")
    print(f"Low Suspicion Result: {score_low}")
    
    assert score_high['risk_level'] == "HIGH"
    assert score_low['risk_level'] == "LOW"
    print("Scoring test passed!")

def test_rag():
    print("\nTesting RAG Module...")
    from services.rag import generate_explanation
    
    text = "This is a sample text for RAG analysis. It should be long enough to create chunks."
    metrics = {"ai_likelihood": 0.7, "burstiness": 0.2, "repetition_score": 0.15, "handwriting_similarity": 0.3}
    
    explanation = generate_explanation(text, metrics)
    print(f"Generated Explanation:\n{explanation}")
    
    assert "AI Likelihood" in explanation
    print("RAG test passed!")

if __name__ == "__main__":
    try:
        test_stylometry()
        test_scoring()
        test_rag()
        print("\nAll basic modules verified successfully!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
