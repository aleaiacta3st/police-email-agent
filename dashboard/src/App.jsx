import { useState } from "react";
import ActionTable from "./components/ActionTable";
import "./App.css";
import ConversationList from "./components/ConversationList";

function App() {
  const [actions, setActions] = useState([]);
  const [conversations, setConversations] = useState({});


  const fetchActions = () => {
    fetch("https://web-production-0c0a3.up.railway.app/actions")
      .then((res) => res.json())
      .then((data) => setActions(data));
  };

  const fetchConversations = () => {
    fetch("https://web-production-0c0a3.up.railway.app/conversations")
      .then((res) => res.json())
      .then((data) => setConversations(data));
  };

  return (
    <div className="dashboard">
      <h1>Dispatch Command Center</h1>
      <p className="subtitle">{actions.length} operations logged</p>
      <button onClick={fetchActions} className="refresh-btn">Refresh</button>
      <ActionTable actions={actions} />
      <button onClick={fetchConversations} className="refresh-btn">Load Conversations</button>
      <ConversationList conversations={conversations} />
    </div>
  );
}

export default App;