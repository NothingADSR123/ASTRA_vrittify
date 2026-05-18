from fastapi import APIRouter, UploadFile, File, Form
from utils.file_handler import save_upload_file, get_sample_path
from services.ocr import extract_text
from services.stylometry import compute_stylometry
from services.handwriting import compute_handwriting_similarity
from services.scoring import calculate_final_score
from services.rag import generate_explanation
import re

router = APIRouter()

@router.post("/upload")
async def upload_assignment(
    file: UploadFile = File(...),
    student_id: str = Form(...)
):
    # 1. Save uploaded file
    file_path = await save_upload_file(file)
    
    # 2. Extract Text (OCR)
    ocr_result = extract_text(file_path)
    full_text = ocr_result["full_text"]
    ocr_success = ocr_result["success"]
    
    has_stylometry_data = False
    # 3. Stylometry Analysis (only if OCR succeeded)
    if ocr_success:
        stylometry_metrics = compute_stylometry(full_text)
        # Check if we actually have stylometry data (not just zeros)
        words = re.findall(r'\w+', full_text.lower())
        sentences = re.split(r'[.!?]+', full_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        has_stylometry_data = len(words) >= 50 and len(sentences) >= 3
    else:
        stylometry_metrics = {
            "ai_likelihood": 0.0,
            "burstiness": 0.0,
            "repetition_score": 0.0
        }
    
    # 4. Handwriting Analysis
    sample_path = get_sample_path(student_id)
    handwriting_similarity = compute_handwriting_similarity(file_path, sample_path)
    
    # 5. Final Scoring
    if ocr_success:
        scoring_result = calculate_final_score(
            stylometry_metrics["ai_likelihood"],
            handwriting_similarity,
            has_stylometry_data
        )
    else:
        scoring_result = {
            "suspicion_score": 0.5,
            "risk_level": "MEDIUM",
            "flags": ["OCR failed - unable to extract text for analysis"]
        }
    
    # 6. RAG Explanation
    metrics_for_rag = {
        **stylometry_metrics,
        "handwriting_similarity": handwriting_similarity
    }
    explanation = generate_explanation(full_text, metrics_for_rag) if ocr_success else "OCR failed to extract text from the document. Please ensure the document is clear and readable, or install Tesseract OCR and Poppler."
    
    # 7. Construct Response
    return {
        "student_id": student_id,
        "ai_likelihood": round(stylometry_metrics["ai_likelihood"], 2),
        "handwriting_similarity": round(handwriting_similarity, 2),
        "suspicion_score": round(scoring_result["suspicion_score"], 2),
        "risk_level": scoring_result["risk_level"],
        "ocr_snippet": ocr_result["snippet"],
        "explanation": explanation,
        "flags": scoring_result["flags"],
        "ocr_success": ocr_success,
        "has_stylometry_data": has_stylometry_data
    }
