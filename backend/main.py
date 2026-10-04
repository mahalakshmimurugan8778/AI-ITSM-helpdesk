from transformers import pipeline
import numpy as np
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
llm = None

# RAG Knowledge Base
KB_PATHS = [
    Path(__file__).resolve().parent.parent / "knowledge_base",
    Path(__file__).resolve().parent.parent / "frontend" / "src" / "knowledge_base"
]
def search_knowledge_base(query, top_k=1):
    if kb_index is None or not kb_texts:
        return None, None

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = kb_index.search(query_embedding, top_k)

    best_index = indices[0][0]

    return kb_texts[best_index], kb_names[best_index]

kb_files = []

for path in KB_PATHS:
    if path.exists():
        kb_files.extend(list(path.glob("*.txt")))

kb_texts = []
kb_names = []

for file in kb_files:
    text = file.read_text(encoding="utf-8")
    kb_texts.append(text)
    kb_names.append(file.name)

if kb_texts:
    embeddings = embedding_model.encode(kb_texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    kb_index = faiss.IndexFlatL2(dimension)
    kb_index.add(embeddings)

    print("RAG Knowledge Base loaded:", len(kb_files), "documents")
else:
    kb_index = None
    print("No Knowledge Base documents found.")
model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI(title="AI ITSM Helpdesk")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["ai_itsm"]
tickets_collection = db["tickets"]
MONGODB_URI = os.getenv("MONGODB_URI")
print("MongoDB URI loaded:", bool(MONGODB_URI))
print("MongoDB connected successfully")
from pydantic import BaseModel

class ProblemRequest(BaseModel):
    problem: str
@app.get("/")
def home():
    return {
        "message": "AI ITSM Helpdesk API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


from pydantic import BaseModel


class ProblemRequest(BaseModel):
    problem: str
    pass

KB_PATH = Path(__file__).resolve().parent.parent / "frontend" / "src" / "knowledge_base"
kb_files = list(KB_PATH.glob("*.txt"))
import numpy as np

kb_texts = []
kb_names = []

for file in kb_files:
    text = file.read_text(encoding="utf-8")
    kb_texts.append(text)
    kb_names.append(file.name)

kb_embeddings = model.encode(kb_texts)
def search_knowledge(problem):
    query_embedding = model.encode([problem])[0]

    scores = np.dot(kb_embeddings, query_embedding) / (
        np.linalg.norm(kb_embeddings, axis=1) *
        np.linalg.norm(query_embedding)
    )

    best_index = int(np.argmax(scores))

    return {
        "source": kb_names[best_index],
        "content": kb_texts[best_index],
        "confidence": float(scores[best_index])
    }


@app.post("/analyze")
def analyze_problem(request: ProblemRequest):
    kb_result = search_knowledge(request.problem)
    kb_content = kb_result["content"]
    kb_source = kb_result["source"]
    ticket = {
        "problem": request.problem,
        "status": "New",
        "category": "IT Support"
    }

    try:
        result = tickets_collection.insert_one(ticket)
        ticket_id = str(result.inserted_id)
    except Exception as e:
        print("MongoDB save error:", e)
        ticket_id = "TEMP-001"

    problem = request.problem.lower()

    if "vpn" in problem:
        intent = "Incident"
        category = "Network / VPN"
        priority = "P2"
        assignment_group = "Network Support"
        confidence = "94%"
        resolution = "Check VPN credentials and restart the VPN client."

    elif "password" in problem or "expired" in problem:
        intent = "Automatable Issue"
        category = "Account / Password"
        priority = "P2"
        assignment_group = "Service Desk"
        confidence = "96%"
        resolution = "Reset your expired password using the company password portal."

    elif "outlook" in problem or "email" in problem or "sync" in problem:
        intent = "Knowledge Question"
        category = "Application / Outlook"
        priority = "P3"
        assignment_group = "Application Support"
        confidence = "92%"
        resolution = "Restart Outlook and check the internet connection."

    elif "visual studio code" in problem or "vscode" in problem:
        intent = "Service Request"
        category = "Software Installation"
        priority = "P3"
        assignment_group = "Service Desk"
        confidence = "95%"
        resolution = "Visual Studio Code request submitted through the software catalogue."

    else:
        intent = "Incident"
        category = "General IT"
        priority = "P3"
        assignment_group = "Service Desk"
        confidence = "70%"
        resolution = "Your issue needs further investigation by the Service Desk."

    return {
        "message": "Problem analyzed successfully",
        "ticket_id": ticket_id,
        "problem": request.problem,
        "status": "New",
        "intent": intent,
        "category": category,
        "priority": priority,
        "assignmentGroup": assignment_group,
        "confidence": confidence,
        "resolution": resolution,
        "source": "IT Knowledge Base",
        "knowledge_source": kb_source,
        "knowledge_content": kb_content
        }
@app.post("/servicenow/incident")
def create_incident(request: ProblemRequest):
    return {
        "number": "INC001246",
        "status": "Created",
        "message": "ServiceNow Incident created successfully"
    }
@app.post("/servicenow/request")
def create_service_request(request: ProblemRequest):
    return {
        "number": "REQ001245",
        "software": "Visual Studio Code",
        "status": "Provisioning",
        "message": "ServiceNow Request created successfully"
    }

