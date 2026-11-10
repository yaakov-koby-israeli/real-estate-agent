// Mirrors the backend endpoints in backend/app/api/chat_routes.py.
// Both return: { session_id, step, text, options }

export class SessionExpiredError extends Error {}

async function post(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (response.status === 404) {
    throw new SessionExpiredError("Chat session not found");
  }
  if (!response.ok) {
    throw new Error(`Chat request failed (${response.status})`);
  }
  return response.json();
}

export function startChat() {
  return post("/api/chat/start");
}

export function sendMessage(sessionId, message) {
  return post("/api/chat/message", { session_id: sessionId, message });
}
