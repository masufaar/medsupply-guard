import os
from unittest.mock import patch
import pandas as pd

import pytest
import requests

from src.llm.gemma_client import GemmaClient, clean_model_output
from src.llm.safety import is_clinical_question

def test_clean_model_output():
    raw1 = "<think>some reasoning</think>\nFinal Answer"
    assert clean_model_output(raw1) == "Final Answer"
    
    raw2 = "Thinking...\nStep 1\nStep 2\n...done thinking.\nThe real answer."
    assert clean_model_output(raw2) == "The real answer."
    
    raw3 = "Thinking Process:\nReasoning\n\nAnswer."
    assert clean_model_output(raw3) == "Answer."
    
    raw4 = "**(Result Generation)**\nDoing stuff\n\nActual output"
    assert clean_model_output(raw4) == "Actual output"

def test_is_clinical_question_positive():
    assert is_clinical_question("Can you diagnose this symptom?") is True
    assert is_clinical_question("What dosage should I prescribe?") is True
    assert is_clinical_question("Are there any side effects to this treatment?") is True
    assert is_clinical_question("Can we substitute treatment X with Y?") is True
    
def test_is_clinical_question_negative():
    assert is_clinical_question("When will the next shipment arrive?") is False
    assert is_clinical_question("What is the current stock level?") is False
    assert is_clinical_question("Please summarize the inventory risk.") is False

@patch.dict(os.environ, {"GEMMA_BACKEND": "mock", "GEMMA_MODEL": "test_model"})
def test_gemma_client_mock_mode():
    client = GemmaClient()
    assert client.backend == "mock"
    assert client.model_name == "test_model"
    
    analytics_row = {
        "medicine_name": "TestMed",
        "current_stock_units": 10,
        "risk_level": "high"
    }
    
    explanation = client.explain_stockout_risk(analytics_row)
    assert "**Medicine:** TestMed" in explanation
    assert "HIGH" in explanation

@patch.dict(os.environ, {"GEMMA_BACKEND": "ollama"})
@patch("src.llm.gemma_client.requests.post")
def test_gemma_client_ollama_failure_graceful(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")
    
    client = GemmaClient()
    assert client.backend == "ollama"
    
    explanation = client.explain_stockout_risk({"medicine_name": "Med A"})
    assert "Error: Unable to connect to Ollama runtime" in explanation
    assert "Connection refused" in explanation

def test_context_preparation():
    client = GemmaClient()
    analytics_row = {
        "medicine_name": "Aspirin",
        "current_stock_units": 50,
        "avg_daily_demand": 5.0,
        "days_of_cover": 10.0,
        "projected_stockout_date": "2026-06-01",
        "risk_level": "medium",
        "recommended_quantity_units": 200,
        "preferred_supplier": "Supplier A",
        "supplier_reason": "Lowest cost",
        "expiry_warning": None,
        "pending_order_notes": None
    }
    
    context = client._prepare_context(analytics_row)
    assert context["medicine_name"] == "Aspirin"
    assert context["current_stock"] == 50
    assert context["average_daily_demand"] == 5.0
    assert context["risk_level"] == "medium"
    assert context["risk_reason"] == "Sufficient stock"
    assert context["safety_boundary"] == "Logistics and procurement support only. Do not provide clinical advice."

@patch.dict(os.environ, {"GEMMA_BACKEND": "mock"})
def test_answer_question_routing():
    client = GemmaClient()
    
    # Clinical question
    response = client.answer_question("What dose should I give?", {})
    
    # Assert it does NOT leak the prompt instructions
    lower_response = response.lower()
    assert "thinking" not in lower_response
    assert "task:" not in lower_response
    assert "response requirements:" not in lower_response
    
    # Assert it contains the required safety messaging
    assert "logistics and procurement only" in lower_response
    assert "can't provide dosage" in lower_response
    assert "consult a licensed clinician or pharmacist" in lower_response
    
    # Logistics question
    response_logistics = client.answer_question("When is the next order coming?", {"medicine_name": "MedA"})
    assert "MedA" in response_logistics

def test_procurement_mock_output():
    client = GemmaClient()
    row = {
        "medicine_name": "Oxy",
        "risk_level": "critical",
        "days_of_cover": 6.1,
        "recommended_quantity_units": 96,
        "preferred_supplier": "MatCare",
        "projected_stockout_date": "2026-05-10"
    }
    client.backend = "mock"
    msg = client.generate_procurement_message(row)
    assert "96" in msg
    assert "Oxy" in msg
    assert "MatCare" in msg
    assert "CRITICAL" in msg
    assert "6.1" in msg
    assert "[Quantity]" not in msg

def test_answer_question_ranked_context():
    client = GemmaClient()
    client.backend = "mock"
    all_res = pd.DataFrame([
        {
            "medicine_name": "Amoxicillin 500mg", 
            "risk_level": "critical", 
            "days_of_cover": 5.1, 
            "recommended_quantity_units": 449, 
            "supplier_reason": "Standard lead time",
            "preferred_supplier": "Supplier B"
        },
        {
            "medicine_name": "Oxytocin Injection", 
            "risk_level": "critical", 
            "days_of_cover": 6.1, 
            "recommended_quantity_units": 96, 
            "supplier_reason": "No supplier can arrive before projected stockout...",
            "preferred_supplier": "MaternalCare Supply"
        }
    ])
    
    # Priority words should trigger the ranked explanation
    response = client.answer_question("Which medicine should we reorder first and why?", {}, all_results=all_res)
    
    assert "Oxytocin Injection" in response
    assert "Amoxicillin 500mg" in response
    assert "Mock Answer" not in response
    assert "no supplier can arrive" in response.lower()
    assert "96" in response

