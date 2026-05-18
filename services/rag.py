from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_explanation(text: str, metrics: dict) -> str:
    """
    Simulates a RAG-based explanation.
    In a real system, this would retrieve context from FAISS and call an LLM.
    """
    if not text:
        return "No text extracted to analyze."

    # Check if we have enough text for stylometry analysis
    words = re.findall(r'\w+', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    has_stylometry_data = len(words) >= 50 and len(sentences) >= 3

    if not has_stylometry_data:
        hw_sim = metrics.get("handwriting_similarity", 0.5)
        explanation = f"Analysis Summary:\n"
        explanation += f"- Insufficient text extracted for stylometry analysis (requires at least 50 words and 3 sentences).\n"
        
        if hw_sim < 0.4:
            explanation += f"- Warning: Handwriting similarity ({hw_sim:.2f}) is low compared to the reference sample, indicating it might not be the same student's work.\n"
        elif hw_sim > 0.8:
            explanation += f"- Note: Handwriting matches the reference sample closely ({hw_sim:.2f}).\n"
        
        explanation += f"\nExtracted Text:\n\"{text[:200]}...\""
        return explanation

    # 1. Chunking
    chunks = [text[i:i+500] for i in range(0, len(text), 400)]
    
    # 2. Embedding & FAISS (Simulated retrieval)
    if chunks:
        embeddings = model.encode(chunks)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        # Simulate a query related to AI patterns
        query = "repetitive sentence structure and low variance"
        query_embedding = model.encode([query])
        D, I = index.search(np.array(query_embedding).astype('float32'), k=1)
        top_chunk = chunks[I[0][0]]
    else:
        top_chunk = "N/A"

    # 3. Generate Explanation (Heuristic-based / Template)
    ai_lik = metrics.get("ai_likelihood", 0)
    burst = metrics.get("burstiness", 0)
    rep = metrics.get("repetition_score", 0)
    hw_sim = metrics.get("handwriting_similarity", 0.5)

    explanation = f"Analysis Summary:\n"
    explanation += f"- The document shows an AI Likelihood of {ai_lik:.2f}.\n"
    
    if burst < 0.5:
        explanation += f"- Warning: Low burstiness ({burst:.2f}) detected. Sentence lengths are very uniform, which is a common trait of AI-generated text.\n"
    else:
        explanation += f"- Note: Burstiness ({burst:.2f}) is within normal human range.\n"

    if rep > 0.1:
        explanation += f"- Warning: High repetition score ({rep:.2f}) suggests potential keyword stuffing or AI patterns.\n"
        
    if hw_sim < 0.4:
        explanation += f"- Warning: Handwriting similarity ({hw_sim:.2f}) is low compared to the reference sample, indicating it might not be the same student's work.\n"
    elif hw_sim > 0.8:
        explanation += f"- Note: Handwriting matches the reference sample closely ({hw_sim:.2f}).\n"

    explanation += f"\nRelevant Text Segment Analyzed:\n\"{top_chunk[:200]}...\""
    
    return explanation
