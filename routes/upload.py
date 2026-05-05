from fastapi import APIRouter, UploadFile, File, Form
from utils.file_handler import save_upload_file, get_sample_path
from services.ocr import extract_text
from services.stylometry import compute_stylometry
from services.handwriting import compute_handwriting_similarity
from services.scoring import calculate_final_score
from services.rag import generate_explanation

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
    
    # 3. Stylometry Analysis
    stylometry_metrics = compute_stylometry(full_text)
    
    # 4. Handwriting Analysis
    sample_path = get_sample_path(student_id)
    handwriting_similarity = compute_handwriting_similarity(file_path, sample_path)
    
    # 5. Final Scoring
    scoring_result = calculate_final_score(
        stylometry_metrics["ai_likelihood"],
        handwriting_similarity
    )
    
    # 6. RAG Explanation
    metrics_for_rag = {
        **stylometry_metrics,
        "handwriting_similarity": handwriting_similarity
    }
    explanation = generate_explanation(full_text, metrics_for_rag)
    
    # 7. Construct Response
    return {
        "student_id": student_id,
        "ai_likelihood": round(stylometry_metrics["ai_likelihood"], 2),
        "handwriting_similarity": round(handwriting_similarity, 2),
        "suspicion_score": round(scoring_result["suspicion_score"], 2),
        "risk_level": scoring_result["risk_level"],
        "ocr_snippet": ocr_result["snippet"],
        "explanation": explanation,
        "flags": scoring_result["flags"]
    }
