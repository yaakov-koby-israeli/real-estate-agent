import { useState } from "react";

const MAX_LENGTH = 1000; // same limit as the backend (MessageRequest in chat_routes.py)

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault(); // a <form> would otherwise reload the whole page
    const trimmed = text.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setText("");
  }

  return (
    <form className="chat__input" onSubmit={handleSubmit}>
      <input
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="כתבו הודעה..."
        maxLength={MAX_LENGTH}
        disabled={disabled}
      />
      <button type="submit" className="button" disabled={disabled || !text.trim()}>
        שליחה
      </button>
    </form>
  );
}
