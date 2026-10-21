# -*- coding: utf-8 -*-
"""RMA Reverse Logistics Triage Router for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class RMAReverseLogisticsTriageRouter:
    @staticmethod
    def evaluate_return_disposition_economics(item_retail_price_usd: float, reverse_shipping_quote_usd: float, refurbish_cost_usd: float = 5.0, secondary_market_salvage_pct: float = 40.0) -> Dict[str, Any]:
        salvage_recovery_usd = item_retail_price_usd * (secondary_market_salvage_pct / 100.0)
        net_return_yield_usd = salvage_recovery_usd - reverse_shipping_quote_usd - refurbish_cost_usd
        
        if net_return_yield_usd <= 0:
            disposition = "CUSTOMER_KEEP_REFUND"
            recommendation = "Offer instant refund or store credit without physical return to eliminate negative logistics margin."
        elif net_return_yield_usd > (item_retail_price_usd * 0.6):
            disposition = "RETURN_TO_PRIMARY_FULFILLMENT"
            recommendation = "Inspect, re-box, and restock to prime inventory."
        else:
            disposition = "DIRECT_TO_SECONDARY_LIQUIDATOR"
            recommendation = "Route directly to B2B liquidation pallet partner."

        return {
            "retail_price_usd": item_retail_price_usd,
            "reverse_freight_usd": reverse_shipping_quote_usd,
            "salvage_recovery_usd": round(salvage_recovery_usd, 2),
            "net_recovery_yield_usd": round(net_return_yield_usd, 2),
            "optimal_disposition": disposition,
            "operational_directive": recommendation
        }

    @staticmethod
    def score_return_abuse_fraud_risk(customer_return_rate_pct: float, rma_reason_code: str, order_age_days: int = 10) -> Dict[str, Any]:
        risk_score = min(100.0, customer_return_rate_pct * 1.5)
        if rma_reason_code.lower() in ["missing_parts", "empty_box", "defective_unverifiable"]:
            risk_score += 25.0
        if order_age_days > 25:
            risk_score += 15.0
        risk_score = round(min(100.0, risk_score), 1)
        
        flag = "HIGH_SCRUTINY_SERIAL_CHECK" if risk_score >= 65.0 else ("MODERATE_AUDIT" if risk_score >= 35.0 else "FRICTIONLESS_AUTO_APPROVE")
        return {"return_rate_pct": customer_return_rate_pct, "abuse_risk_score": risk_score, "triage_status": flag, "inspection_action": "Require unboxing photo and carrier weight scan verification." if risk_score >= 65.0 else "Standard RMA slip."}
