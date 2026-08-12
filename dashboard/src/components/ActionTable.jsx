function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });
}

function getToolClass(toolName) {
  if (toolName === "request_ambulance") return "tool-ambulance";
  if (toolName === "freeze_account") return "tool-freeze";
  if (toolName === "alert_nearby_units") return "tool-alert";
  return "";
}

function formatToolName(toolName) {
  return toolName.replace(/_/g, " ").toUpperCase();
}

function ActionTable({ actions }) {
  return (
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>Case ID</th>
          <th>Tool</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {actions.map((action) => (
          <tr key={action.id}>
            <td>{formatTime(action.timestamp)}</td>
            <td>{action.case_id}</td>
            <td className={getToolClass(action.tool_name)}>
              {formatToolName(action.tool_name)}
            </td>
            <td>{action.details}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ActionTable;