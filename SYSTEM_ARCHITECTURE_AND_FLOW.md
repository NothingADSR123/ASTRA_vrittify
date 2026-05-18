# ASTRA System Architecture & Flow

## Overview

ASTRA (Advanced Stylometric & Textual Recognition Analysis) is an enterprise-grade AI platform designed to verify the authenticity of student assignments by analyzing both textual and visual characteristics.

---

## Table of Contents
1. [Complete Workflow](#complete-workflow)
2. [Backend Modules](#backend-modules)
3. [Frontend Flow](#frontend-flow)
4. [OCR Pipeline](#ocr-pipeline)
5. [Stylometry Logic](#stylometry-logic)
6. [Handwriting Verification](#handwriting-verification)
7. [RAG Explanation System](#rag-explanation-system)
8. [Scoring System](#scoring-system)
9. [API Flow](#api-flow)
10. [Folder Structure](#folder-structure)
11. [Tech Stack](#tech-stack)
12. [Data Flow](#data-flow)
13. [Limitations](#limitations)
14. [Future Improvements](#future-improvements)

---

## Complete Workflow

```
┌─────────────────┐
│   Landing Page  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Fake Login UI  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Main Dashboard │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Upload & Analyze│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Processing Anim. │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Intelligence Rep.│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Analytics & Logs │
└─────────────────┘
```

---

## Backend Modules

### 1. Main Application (`main.py`)
- FastAPI entry point
- Serves static files and API routes
- Runs on `http://localhost:8000`

### 2. Routes (`routes/upload.py`)
- `/upload` API endpoint
- Orchestrates entire analysis pipeline

### 3. Services Layer
- **OCR Service** (`services/ocr.py`): Extracts text from images/PDFs using Tesseract
- **Stylometry Service** (`services/stylometry.py`): Computes AI likelihood based on burstiness and repetition
- **Handwriting Service** (`services/handwriting.py`): Compares document with reference sample using OpenCV
- **Scoring Service** (`services/scoring.py`): Combines signals into final suspicion score
- **RAG Service** (`services/rag.py`): Generates explainable insights using sentence transformers

### 4. Utilities (`utils/file_handler.py`)
- Saves uploaded files to `data/uploads/`
- Retrieves student reference samples from `data/samples/`

---

## Frontend Flow

### Pages:
1. **Landing Page**: Hero section, features, workflow, CTA buttons
2. **Fake Login**: Institution ID, email, password (no real auth)
3. **Main Dashboard**: Sidebar, system status, recent activity
4. **Upload & Analyze**: File upload form
5. **Processing Animation**: Animated stages of analysis
6. **Intelligence Report**: Detailed analysis results
7. **Analytics Dashboard**: Charts and metrics
8. **History & Logs**: Fake history table and system logs

---

## OCR Pipeline

```
Input File (Image/PDF)
       ↓
Extract Extension
       ↓
PDF? ── Yes → Convert to images (Poppler)
       ↓ No
Image Processing (PIL)
       ↓
Text Extraction (Tesseract)
       ↓
Check text quality (≥20 chars)
       ↓
Return { full_text, snippet, success }
```

**Key Features:**
- Auto-detects Tesseract path on Windows
- Handles both images (PNG/JPG/JPEG/BMP/TIFF) and PDFs
- Returns success flag indicating whether meaningful text was extracted

---

## Stylometry Logic

### Heuristics Used:
1. **Burstiness**: Measures sentence length variance
   - High burstiness = More human-like
   - Low burstiness = More AI-like (uniform sentence lengths)
   - Formula: `std_dev(sentence_lengths) / mean(sentence_lengths)`

2. **Repetition Score**: Ratio of repeated words
   - Higher repetition = More AI-like
   - Formula: `(total_words - unique_words) / total_words`

3. **AI Likelihood**: Combined score
   - Formula: `(1 - min(burstiness, 1.0)) + (repetition_score * 0.04)`
   - Range: 0.0 (definitely human) → 1.0 (definitely AI)

### Requirements for Analysis:
- ≥50 words total
- ≥3 complete sentences

---

## Handwriting Verification

### Algorithm:
1. Load both images (submitted + reference sample)
2. Convert to grayscale
3. Resize to 500x500 pixels
4. Apply Canny edge detection (100-200 thresholds)
5. Compute pixel-wise difference between edge maps
6. Calculate similarity: `1 - (mean_difference / 255)`

### Output:
- Range: 0.0 (completely different) → 1.0 (identical)
- Returns 0.5 if reference sample not found

---

## RAG Explanation System

### Components:
1. **Chunking**: Splits text into 500-character chunks with 100-character overlap
2. **Embeddings**: Uses `all-MiniLM-L6-v2` sentence transformer
3. **Vector Search**: FAISS IndexFlatL2 for similarity search
4. **Explanation Generation**: Template-based explanation with metrics

### Key Features:
- Simulates RAG without actual knowledge base
- Generates structured, human-readable insights
- Includes relevant text segments from the document

---

## Scoring System

### Final Suspicion Score Formula:

**With Stylometry Data:**
```
final_score = 0.6 * ai_likelihood + 0.3 * handwriting_suspicion + 0.1
where handwriting_suspicion = 1 - handwriting_similarity
```

**Without Stylometry Data:**
```
final_score = 0.5 * handwriting_suspicion + 0.25
```

### Risk Levels:
- **LOW**: 0.00 – 0.35
- **MEDIUM**: 0.35 – 0.65
- **HIGH**: 0.65 – 1.00

### Flags:
- "High AI likelihood detected" (ai_likelihood > 0.6)
- "Significant handwriting deviation" (handwriting_similarity < 0.4)
- "Insufficient text for stylometry analysis"
- "OCR failed - unable to extract text for analysis"

---

## API Flow

### Endpoint: `POST /upload`

#### Request:
```
multipart/form-data:
- file: Image/PDF file
- student_id: String identifier for student
```

#### Response:
```json
{
  "student_id": "student123",
  "ai_likelihood": 0.89,
  "handwriting_similarity": 0.82,
  "suspicion_score": 0.69,
  "risk_level": "HIGH",
  "ocr_snippet": "Relevant text snippet...",
  "explanation": "Detailed analysis explanation...",
  "flags": ["High AI likelihood detected"],
  "ocr_success": true,
  "has_stylometry_data": true
}
```

---

## Folder Structure

```
ASTRA_prototype/
├── main.py                          # FastAPI entry point
├── routes/
│   └── upload.py                    # Upload API endpoint
├── services/
│   ├── ocr.py                       # OCR text extraction
│   ├── stylometry.py                # Stylometric analysis
│   ├── handwriting.py               # Handwriting similarity
│   ├── scoring.py                   # Final scoring logic
│   └── rag.py                       # RAG explanation generator
├── utils/
│   └── file_handler.py              # File handling utilities
├── data/
│   ├── uploads/                     # Uploaded documents
│   └── samples/                     # Student reference samples
├── static/
│   └── index.html                   # Original simple frontend
├── requirements.txt                 # Python dependencies
├── verify_setup.py                  # Setup verification script
├── create_samples.py                # Create sample reference data
└── SYSTEM_ARCHITECTURE_AND_FLOW.md # This document
```

---

## Tech Stack

### Backend:
- **FastAPI**: Modern, high-performance web framework
- **Python 3.10+**: Core programming language
- **Uvicorn**: ASGI server

### AI/Processing:
- **pytesseract**: OCR text extraction
- **pdf2image**: PDF to image conversion
- **OpenCV**: Image processing for handwriting verification
- **NumPy**: Numerical computations
- **Sentence-Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **Pillow**: Image processing

### Frontend (Planned):
- **React**: UI library
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations
- **Recharts**: Data visualization
- **Lucide Icons**: Modern icon set

---

## Data Flow

```
User Uploads File
       ↓
Save to data/uploads/
       ↓
Extract Text via OCR
       ↓
Stylometry Analysis (if enough text)
       ↓
Handwriting Similarity Check
       ↓
Calculate Final Score
       ↓
Generate RAG Explanation
       ↓
Return JSON Response
       ↓
Display in Frontend
```

---

## Limitations

### MVP Limitations:
1. **Heuristic-based detection**: No ML-trained models
2. **Basic handwriting comparison**: Uses edge detection only (no deep embeddings)
3. **Limited OCR robustness**: Struggles with low-quality images
4. **No real authentication**: Fake login UI only
5. **No persistent database**: No user/history storage
6. **Single-user system**: No multi-tenant support
7. **English-only**: No multilingual support

---

## Future Improvements

### Short-term:
- Better OCR preprocessing (deskewing, noise reduction)
- Improved handwriting verification with CNN embeddings
- User session management
- Basic history storage

### Medium-term:
- Siamese networks for identity verification
- Advanced stylometric modeling
- Multilingual normalization
- Real database integration
- Batch processing

### Long-term:
- Institutional analytics dashboard
- Real-time processing
- API for third-party integrations
- Advanced ML models for detection
- Mobile app support

---

## Conclusion

This document provides a comprehensive overview of the ASTRA system architecture and data flow. The current implementation is a functioning MVP that demonstrates the complete end-to-end pipeline for authorship verification using lightweight techniques and explainable AI. While simplified, it establishes a strong foundation for scaling into a full forensic-grade system.
