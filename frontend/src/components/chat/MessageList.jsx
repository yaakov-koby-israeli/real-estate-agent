import { useEffect, useRef } from "react";

export default function MessageList({ messages }) {
  const containerRef = useRef(null);

  // After every new message, scroll the messages area (not the whole page) to the bottom.
  useEffect(() => {
    const container = containerRef.current;
    container.scrollTo({ top: container.scrollHeight, behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat__messages" ref={containerRef}>
      {messages.map((message, index) => (
        // Messages are only ever appended, never reordered - so the index is a stable key here.
        <div key={index} className={`chat__message chat__message--${message.role}`}>
          {message.text}
        </div>
      ))}
    </div>
  );
}
