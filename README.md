# PulseQueue Engine ⚡

[![Tests](https://github.com/<YOUR_GITHUB_USERNAME>/pulse-queue/actions/workflows/test.yml/badge.svg)](https://github.com/<YOUR_GITHUB_USERNAME>/pulse-queue/actions)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Framework](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)
![Database](https://img.shields.io/badge/SQLAlchemy-Async-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A high-throughput asynchronous webhook ingestion and event processing engine built with **FastAPI**, **SQLAlchemy (Async)**, and **Pydantic v2**. 

PulseQueue accepts incoming event streams, sensor telemetry, and third-party webhooks with sub-10ms latency, delegates business logic to background workers, guarantees data persistence via an async database layer, and provides real-time system metrics.

---

## Key Features

* **Non-Blocking Ingestion:** Returns an immediate `202 Accepted` response with an auto-generated UUID while offloading serialization and storage to asynchronous background workers.
* **Strict Payload Validation:** Powered by Pydantic v2 schemas enforcing typed models, source verification, dynamic timestamps, and priority categorization (`low`, `medium`, `high`, `critical`).
* **Header-Based Authentication:** Protects ingestion routes from unauthorized flooding using a custom `X-Pulse-Key` header verification scheme.
* **Async Persistence Layer:** Non-blocking async database sessions via SQLAlchemy and SQLite/PostgreSQL with automatic table creation during application lifespan.
* **Automated CI/CD Pipeline:** Fully covered by an asynchronous `pytest` + `httpx` test suite executed on every pull request and push via GitHub Actions.

---

## Architecture Flow

```text
[ Webhook / IoT Device ]
           │
           │  POST /api/v1/events/ingest  (Header: X-Pulse-Key)
           ▼
┌────────────────────────────────────────────────────────┐
│                    FastAPI Engine                      │
│  ├── API Key Security Guard                            │
│  └── Pydantic v2 Payload Validation                   │
└────────────────────────────────────────────────────────┘
           │
           ├──────────────────────────────► [ 202 Accepted (<10ms) ]
           │
           ▼ (Background Tasks Runner)
┌────────────────────────────────────────────────────────┐
│                   Worker Pipeline                      │
│  ├── Priority Tier Classifier                          │
│  └── SQLAlchemy Async Session Manager                  │
└────────────────────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────────────────────┐
│                  Persistent Database                   │
└────────────────────────────────────────────────────────┘
           ▲
           │ Query Access
┌────────────────────────────────────────────────────────┐
│  • GET /api/v1/events/metrics                          │
│  • GET /api/v1/events/recent?limit=10                  │
└────────────────────────────────────────────────────────┘