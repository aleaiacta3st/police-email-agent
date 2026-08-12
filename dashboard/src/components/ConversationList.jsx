import { useState } from "react";

function ConversationList({ conversations }) {
  const [openCases, setOpenCases] = useState(new Set());

  const toggleCase = (caseId) => {
    const next = new Set(openCases);
    if (next.has(caseId)) {
      next.delete(caseId);
    } else {
      next.add(caseId);
    }
    setOpenCases(next);
  };

  const caseIds = Object.keys(conversations);

  return (
    <div className="conversations">
      <h2>Case Conversations</h2>
      {caseIds.map((caseId) => (
        <div key={caseId} className="case">
          <div className="case-header" onClick={() => toggleCase(caseId)}>
            <span>{caseId}</span>
            <span>{openCases.has(caseId) ? "▲" : "▼"}</span>
          </div>
          {openCases.has(caseId) && (
            <div className="case-messages">
              {conversations[caseId].map((msg, i) => (
                <div key={i} className={`message ${msg.role}`}>
                  <strong>{msg.role === "user" ? "Victim" : "Officer"}</strong>
                  <p>{msg.content}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default ConversationList;