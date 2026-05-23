"""
AI Layer untuk Smart Drafting Engine
Menggunakan Groq (LLaMA 3) untuk:
1. Document Classification (Invoice / B/L / Packing List)
2. Intelligent Field Extraction (NER dari raw OCR text)
3. Data Validation & Correction
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Groq API Key (fallback, prefer key from request)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")


def get_client(api_key=None):
    """Get Groq client with provided or env API key"""
    key = api_key or GROQ_API_KEY
    if not key:
        return None
    return Groq(api_key=key)


def classify_document(raw_text: str, api_key=None) -> dict:
    """
    AI Document Classification
    Classify document type: Invoice, Bill of Lading, Packing List, or Unknown
    """
    c = get_client(api_key)
    if not c:
        return {"type": "unknown", "confidence": 0, "ai_enabled": False}

    prompt = f"""You are a customs document classifier. Based on the OCR text below, classify the document type.

Respond ONLY with a JSON object (no markdown, no explanation):
{{"type": "invoice" | "bill_of_lading" | "packing_list" | "unknown", "confidence": 0-100, "reason": "brief reason"}}

OCR Text (first 1500 chars):
{raw_text[:1500]}"""

    try:
        response = c.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=150
        )
        result = response.choices[0].message.content.strip()
        # Parse JSON from response
        parsed = json.loads(result)
        parsed["ai_enabled"] = True
        return parsed
    except Exception as e:
        return {"type": "unknown", "confidence": 0, "ai_enabled": False, "error": str(e)}


def extract_fields_ai(raw_text: str, doc_type: str = "invoice", api_key=None) -> list:
    """
    AI-powered Field Extraction
    Uses LLM to extract structured fields from raw OCR text
    """
    c = get_client(api_key)
    if not c:
        return []

    field_spec = {
        "invoice": [
            "invoice_number", "invoice_date", "supplier_name", "consignee",
            "total_amount", "currency", "hs_code", "weight_kg",
            "quantity", "country_of_origin", "bl_number", "vessel_name",
            "port_of_loading", "port_of_discharge", "description_of_goods",
            "terms_of_payment", "incoterms"
        ],
        "bill_of_lading": [
            "bl_number", "shipper", "consignee", "notify_party",
            "vessel_name", "voyage_number", "port_of_loading", "port_of_discharge",
            "container_number", "total_packages", "gross_weight_kg",
            "measurement_cbm", "description_of_goods", "freight_status",
            "date_of_issue", "place_of_issue"
        ],
        "packing_list": [
            "invoice_number", "date", "shipper", "consignee",
            "total_packages", "total_gross_weight_kg", "total_net_weight_kg",
            "total_measurement_cbm", "marks_and_numbers", "description_of_goods"
        ]
    }

    fields = field_spec.get(doc_type, field_spec["invoice"])

    prompt = f"""You are an AI assistant for customs document processing. Extract structured data from this OCR text of a {doc_type.replace('_', ' ')}.

Extract these fields: {', '.join(fields)}

Rules:
- Return ONLY a JSON array of objects
- Each object: {{"field": "field_name", "value": "extracted value", "confidence": 0-100}}
- If a field is not found, set value to null and confidence to 0
- Clean up OCR artifacts (fix obvious typos, remove garbage characters)
- For amounts, include currency symbol
- For HS codes, ensure 8-10 digits
- For dates, use format DD/MM/YYYY or as found in document
- No markdown, no explanation, ONLY the JSON array

OCR Text:
{raw_text[:3000]}"""

    try:
        response = c.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1500
        )
        result = response.choices[0].message.content.strip()
        
        # Try to parse JSON - handle cases where LLM wraps in markdown
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        
        parsed = json.loads(result)
        
        # Add metadata
        for field in parsed:
            field["source"] = "ai"
            field["status"] = (
                "auto_filled" if field.get("confidence", 0) >= 90
                else "review" if field.get("confidence", 0) >= 70
                else "manual"
            )
        
        return parsed
    except Exception as e:
        return [{"error": str(e), "source": "ai"}]


def validate_and_correct(fields: list, raw_text: str, api_key=None) -> list:
    """
    AI Validation & Correction
    Cross-check extracted fields and suggest corrections
    """
    c = get_client(api_key)
    if not c:
        return fields

    fields_json = json.dumps(fields, indent=2)

    prompt = f"""You are a customs document validation AI. Review these extracted fields and correct any errors.

Extracted fields:
{fields_json}

Original OCR text (first 2000 chars):
{raw_text[:2000]}

Rules:
- Return the SAME JSON array structure with corrections applied
- If a value looks wrong based on context, fix it and lower confidence to 75
- If a value is correct, keep confidence as-is or raise it
- Add "corrected": true if you changed a value, "corrected": false otherwise
- No markdown, no explanation, ONLY the JSON array

Return corrected JSON array:"""

    try:
        response = c.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000
        )
        result = response.choices[0].message.content.strip()
        
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        
        return json.loads(result)
    except:
        return fields


def process_with_ai(raw_text: str, api_key=None) -> dict:
    """
    Full AI pipeline:
    1. Classify document
    2. Extract fields using AI
    3. Validate & correct
    """
    key = api_key or GROQ_API_KEY
    if not key:
        return {
            "ai_enabled": False,
            "message": "No API key. Set key in Settings (⚙️ button).",
            "classification": None,
            "fields": []
        }

    # Step 1: Classify
    classification = classify_document(raw_text, api_key=key)
    doc_type = classification.get("type", "invoice")

    # Step 2: Extract
    fields = extract_fields_ai(raw_text, doc_type, api_key=key)

    # Step 3: Validate (skip if extraction failed)
    if fields and not any("error" in f for f in fields):
        fields = validate_and_correct(fields, raw_text, api_key=key)

    return {
        "ai_enabled": True,
        "model": "llama-3.1-8b-instant (Groq)",
        "classification": classification,
        "fields": fields,
        "total_fields": len([f for f in fields if f.get("value")]),
    }
