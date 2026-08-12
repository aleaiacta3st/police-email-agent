import { useState } from "react";

function ConversationList({ conversations }) {
  const [openCase, setOpenCase] = useState(null);

  const caseIds = Object.keys(conversations);

  return (
    <div className="conversations">
      <h2>Case Conversations</h2>
      {caseIds.map((caseId) => (
        <div key={caseId} className="case">
          <div
            className="case-header"
            onClick={() => setOpenCase(openCase === caseId ? null : caseId)}
          >
            <span>{caseId}</span>
            <span>{openCase === caseId ? "▲" : "▼"}</span>
          </div>
          {openCase === caseId && (
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