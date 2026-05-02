# 🚀 Scalable URL Shortener Service (Backend)

A production-grade URL shortening and analytics service built with high-performance system design principles. This project focuses on idempotent API design, database optimization, and efficient request lifecycles.

## 🏗️ System Architecture
The system utilizes a layered architecture to maintain a strict Separation of Concerns (SoC):
- **API Layer:** FastAPI (ASGI) for high-concurrency asynchronous request handling.
- **Validation Layer:** Pydantic models to ensure data integrity and machine-readable error contracts.
- **Persistence Layer:** SQLAlchemy ORM with PostgreSQL for transactional reliability.
- **Dependency Injection:** Request-scoped database sessions to ensure thread safety and prevent memory leaks.

## 🛠️ Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Environment:** Python 3.12+
- **Version Control:** Git/GitHub

## ✨ Key Engineering Features
- **Idempotent API Design:** Optimized the `/shorten` endpoint to prevent duplicate record generation. The system performs a lookup before writing, ensuring consistent mappings and reduced DB bloat.
- **Collision-Safe Generation:** Implemented a retry-loop logic with Base62 character sets, providing a keyspace of ~56 billion unique combinations.
- **Real-time Analytics:** Integrated mutable state tracking to record URL engagement (clicks) without sacrificing redirect speed.
- **High-Performance Lookups:** Applied B-Tree indexing on the `short_code` column, reducing query complexity from O(n) to O(log n).

## 📊 Performance & Optimization Metrics
| Scenario | Initial Latency | Optimized Latency | Improvement |
| :--- | :--- | :--- | :--- |
| First-time URL Creation | ~2.6s (Cold Start) | ~25ms | N/A |
| **Repeated Request** | **~25ms** | **~8ms** | **~68% Reduction** |

## 🚀 Getting Started
1. Clone the repository.
2. Initialize virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Configure `.env` with your `DATABASE_URL`.
5. Start server: `uvicorn app.main:app --reload`.
