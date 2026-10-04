# AI ITSM Helpdesk

AI-powered ITSM and Intelligent Helpdesk Automation Platform.

## Features

- AI-based IT ticket classification
- VPN troubleshooting
- Password reset automation
- Outlook troubleshooting
- Software provisioning request
- Knowledge Base with RAG
- Human escalation for low-confidence requests
- Mock ServiceNow integration

## Technology Stack

- Frontend: React.js
- Backend: Python + FastAPI
- Database: MongoDB Atlas
- Embeddings: Sentence Transformers
- Vector Database: FAISS
- LLM: Hugging Face
- ITSM: ServiceNow / Mock ServiceNow API

## Knowledge Base

The system uses IT support documents for:
- VPN Troubleshooting
- Password Reset
- Outlook Troubleshooting
- Wi-Fi Troubleshooting
- Laptop Performance
- Software Installation
- Application Access

## Test Scenarios

1. VPN connection failure
2. Password expired
3. Outlook synchronization issue
4. Visual Studio Code request
5. Unsupported IT question

## Project Structure

```text
AI-ITSM-helpdesk/
├── backend/
├── frontend/
│   └── src/
│       └── knowledge_base/
└── README.md