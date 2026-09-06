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

## API Reference

### System Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | System health check and service status | No |
| `GET` | `/docs` | Interactive OpenAPI / Swagger UI | No |

### Event Management

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/events/ingest` | Ingest and queue incoming event payloads | **Yes** (`X-Pulse-Key`) |
| `GET` | `/api/v1/events/metrics` | Fetch aggregated counts of processed events | No |
| `GET` | `/api/v1/events/recent` | Fetch paginated recent event payloads | No |

---

## Example Ingestion Payload

```json
{
  "source": "sensor_node_01",
  "event_type": "telemetry_ping",
  "priority": "high",
  "payload": {
    "battery_voltage": 12.4,
    "temperature": 34.2,
    "status": "active"
  }
}
```
## Expected Response (202 Accepted)

```json
{
  "status": "accepted",
  "event_id": "7a41da6f-798e-4a6c-bc43-2615ce675c94",
  "message": "Event received and queued for asynchronous processing",
  "received_at": "2026-09-06T12:00:00Z"
}
```

## Getting Started

### Prerequisites

* Python 3.11 or higher
* Git

### Installation

1. Clone the Repository :
```
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/pulse-queue.git
cd pulse-queue
```
2. Create and activate a virtual environment:
   
   *   Windows (PowerShell):
       ```
       python -m venv venv
       .\venv\Scripts\Activate.ps1
       ```
   *   Linux / macOS:
       ```
       python3 -m venv venv
       source venv/bin/activate
       ```
 
3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the local development server:
```
uvicorn app.main:app --reload
```

5. Access the interactive Swagger documentation at http://127.0.0.1:8000/docs.

## Running Automated Tests:

### Run the asynchronous test suite using pytest

```
pytest
```

## Environment Configuration

###  Create an optional .env file in the project root to configure security keys:

```
PULSE_API_KEY=pulse_dev_secret_key_123
```

## License

### Distributed under the MIT License. See LICENSE for details.

```
---

### Push the Full File

Save the file (`Ctrl + S`), then run this in your PyCharm terminal:

```powershell
git add README.md
git commit -m "docs: complete readme api reference and setup guide"
git push origin main
```

## Example Ingestion Payload

```json
{
  "source": "sensor_node_01",
  "event_type": "telemetry_ping",
  "priority": "high",
  "payload": {
    "battery_voltage": 12.4,
    "temperature": 34.2,
    "status": "active"
  }
}