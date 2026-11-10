import { useEffect, useRef } from "react";
import MessageText from "./MessageText";

export default function MessageList({ messages, isTyping }) {
  const containerRef = useRef(null);

  // After every new message (or when the typing bubble appears), scroll the messages area to the bottom.
  useEffect(() => {
    const container = containerRef.current;
    container.scrollTo({ top: container.scrollHeight, behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="chat__messages" ref={containerRef}>
      {messages.map((message, index) => (
        // Messages are only ever appended, never reordered - so the index is a stable key here.
        <div key={index} className={`chat__message chat__message--${message.role}`}>
          {message.role === "bot" ? <MessageText text={message.text} /> : message.text}
        </div>
      ))}
      {isTyping && (
        <div className="chat__message chat__message--bot chat__typing" aria-label="הסוכן מקליד">
          <span /><span /><span />
        </div>
      )}
    </div>
  );
}
