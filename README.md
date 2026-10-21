# RMA Reverse Logistics Intelligent Triage & Salvage Router Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

RMA disposition router, return shipping cost vs salvage liquidation value, restocking fee calculator, and fraudulent return risk scorer. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `evaluate_return_disposition_economics`: Determine optimal return disposition (Return-to-Stock, Liquidate, Customer Keep) based on net recovery economics.
- `score_return_abuse_fraud_risk`: Score probability of wardrobing, brick-in-box, or return fraud based on customer telemetry.

## 🚀 Installation & Usage
```bash
python -m genpark_agentic_commerce_rma_reverse_logistics_triage_skill.server --test
```
