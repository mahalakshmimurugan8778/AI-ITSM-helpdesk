import { useState } from "react";
const analyzeWithBackend = async (problem) => {
  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ problem }),
  });

  return await response.json();
};
import "./App.css";

function App() {
  const createIncident = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/servicenow/incident", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        problem: problem
      })
    });

    const data = await response.json();

    alert(`${data.message} ${data.number}`);
  } catch (error) {
    console.error(error);
    alert("ServiceNow connection failed");
  }
};
  const [problem, setProblem] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const analyzeProblem = async () => {
  try {
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        problem: problem,
      }),
    });

    const data = await response.json();

    setAnalysis(data);
  } catch (error) {
    console.error(error);
    alert("Backend connection failed");
  }
};
const createServiceRequest = async () => {
  const response = await fetch("http://localhost:8000/servicenow/request", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      problem: problem
    })
  });

  const data = await response.json();

  alert(`${data.message} ${data.number}`);
};

  return (
    <div className="app">
      <h1>AI ITSM Helpdesk</h1>

      <div className="assistant">
        <h2>AI Assistant</h2>

        <p>
          Describe your IT problem and I'll help you find a solution.
        </p>

        <textarea
          rows="5"
          placeholder="Example: I cannot connect to VPN since this morning..."
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
        />

        <br />

        <button onClick={analyzeProblem}>
          Analyze My Problem
        </button>

        {analysis && (
          <div className="analysis">
            <h2>AI Analysis</h2>

            <p><strong>Intent:</strong> {analysis.intent}</p>
            <p><strong>Category:</strong> {analysis.category}</p>
            <p><strong>Priority:</strong> {analysis.priority}</p>
            <p>
              <strong>Assignment Group:</strong>{" "}
              <p>
  <strong>Knowledge Source:</strong> {analysis.knowledge_source}
</p>
              {analysis.assignmentGroup}
            </p>
            <p><strong>Confidence:</strong> {analysis.confidence}</p>
            <p>
              <strong>Suggested Resolution:</strong>{" "}
              {analysis.resolution}
              <p>
  <strong>Source:</strong> IT Knowledge Base
</p>
            </p>
            {analysis.intent === "Automatable Issue" && (
  <button onClick={() => alert("Password reset automation completed successfully!")}>
    Run Auto-Resolution
  </button>
)}
{analysis.intent === "Incident" && analysis.confidence !== "70%" && (
  <button onClick = {createIncident}>
    Create ServiceNow Incident
  </button>
)}
{analysis.intent === "Service Request" && (
  <button onClick = {createServiceRequest}>
    Create Software Service Request
  </button>
)}
          {analysis.confidence === "70%" && (
  <button onClick={() => alert("Escalated to Human Support")}>
    Escalate to Human Support
    </button>
)}
</div>
        )}
      </div>
    </div>
  );
}

export default App;