# -*- coding: utf-8 -*-
"""MCP Server for RMA Reverse Logistics Intelligent Triage & Salvage Router Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import RMAReverseLogisticsTriageRouter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "evaluate_return_disposition_economics",
        "description": "Determine optimal return disposition (Return-to-Stock, Liquidate, Customer Keep) based on net recovery economics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "item_retail_price_usd": {
                    "type": "number"
                },
                "reverse_shipping_quote_usd": {
                    "type": "number"
                },
                "refurbish_cost_usd": {
                    "type": "number"
                },
                "secondary_market_salvage_pct": {
                    "type": "number"
                }
            },
            "required": [
                "item_retail_price_usd",
                "reverse_shipping_quote_usd"
            ]
        }
    },
    {
        "name": "score_return_abuse_fraud_risk",
        "description": "Score probability of wardrobing, brick-in-box, or return fraud based on customer telemetry.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_return_rate_pct": {
                    "type": "number"
                },
                "rma_reason_code": {
                    "type": "string"
                },
                "order_age_days": {
                    "type": "integer"
                }
            },
            "required": [
                "customer_return_rate_pct",
                "rma_reason_code"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-rma-reverse-logistics-triage-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(RMAReverseLogisticsTriageRouter, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-rma-reverse-logistics-triage-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
