import { useState } from "react";
import ActionTable from "./components/ActionTable";
import "./App.css";

function App() {
  const [actions, setActions] = useState([]);

  const fetchActions = () => {
    fetch("https://web-production-0c0a3.up.railway.app/actions")
      .then((res) => res.json())
      .then((data) => setActions(data));
  };

  return (
    <div className="dashboard">
      <h1>Dispatch Command Center</h1>
      <p className="subtitle">{actions.length} operations logged</p>
      <button onClick={fetchActions} className="refresh-btn">Refresh</button>
      <ActionTable actions={actions} />
    </div>
  );
}

export default App;