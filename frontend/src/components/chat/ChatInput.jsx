import { useEffect, useRef, useState } from "react";

const MAX_LENGTH = 1000; // same limit as the backend (MessageRequest in chat_routes.py)

// `disabled`: the input itself is off (conversation finished / not started).
// `canSend`: typing is allowed, but sending waits until the bot has answered.
// We don't disable the input while waiting - the browser drops focus from disabled elements.
export default function ChatInput({ onSend, disabled, canSend }) {
  const [text, setText] = useState("");
  const inputRef = useRef(null);

  // Every time the bot finishes answering, put the cursor back in the input -
  // also after clicking an option button, which takes the focus and then disappears.
  useEffect(() => {
    if (!disabled && canSend) inputRef.current.focus();
  }, [disabled, canSend]);

  function handleSubmit(event) {
    event.preventDefault(); // a <form> would otherwise reload the whole page
    const trimmed = text.trim();
    if (!trimmed || !canSend) return;
    onSend(trimmed);
    setText("");
  }

  return (
    <form className="chat__input" onSubmit={handleSubmit}>
      <input
        ref={inputRef}
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="כתבו הודעה..."
        maxLength={MAX_LENGTH}
        disabled={disabled}
      />
      <button type="submit" className="button" disabled={disabled || !canSend || !text.trim()}>
        שליחה
      </button>
    </form>
  );
}
