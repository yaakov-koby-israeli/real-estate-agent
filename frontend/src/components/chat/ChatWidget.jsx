import { useState } from "react";
import { SessionExpiredError, sendMessage, startChat } from "../../api/chatApi";
import ChatInput from "./ChatInput";
import MessageList from "./MessageList";
import OptionButtons from "./OptionButtons";
import "./ChatWidget.css";

const ERROR_TEXT = "מצטערים, משהו השתבש. נסו שוב בעוד רגע.";
const RESTART_TEXT = "השיחה התאפסה, מתחילים מחדש 🙂";

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [options, setOptions] = useState([]);
  const [step, setStep] = useState(null);
  const [isWaiting, setIsWaiting] = useState(false);

  function addMessage(role, text) {
    setMessages((prev) => [...prev, { role, text }]);
  }

  function applyResponse(data) {
    setSessionId(data.session_id);
    setStep(data.step);
    setOptions(data.options);
    addMessage("bot", data.text);
  }

  async function begin() {
    setIsWaiting(true);
    try {
      applyResponse(await startChat());
    } catch {
      addMessage("bot", ERROR_TEXT);
    } finally {
      setIsWaiting(false);
    }
  }

  function open() {
    setIsOpen(true);
    if (!sessionId && !isWaiting) begin();
  }

  async function send(text) {
    addMessage("user", text);
    setOptions([]);
    setIsWaiting(true);
    try {
      applyResponse(await sendMessage(sessionId, text));
    } catch (error) {
      if (error instanceof SessionExpiredError) {
        addMessage("bot", RESTART_TEXT);
        await begin(); // await, so `finally` below runs only after the new session is ready
        return;
      }
      addMessage("bot", ERROR_TEXT);
    } finally {
      setIsWaiting(false);
    }
  }

  if (!isOpen) {
    return (
      <button className="chat-launcher" onClick={open} aria-label="פתיחת צ'אט עם הסוכן הווירטואלי">
        💬
      </button>
    );
  }

  const isDone = step === "done";

  return (
    <div className="chat">
      <div className="chat__header">
        <span>הסוכן הווירטואלי של פרשקובסקי</span>
        <button className="chat__close" onClick={() => setIsOpen(false)} aria-label="סגירה">✕</button>
      </div>
      <MessageList messages={messages} isTyping={isWaiting} />
      <OptionButtons options={options} onSelect={send} disabled={isWaiting} />
      <ChatInput onSend={send} disabled={isDone || !sessionId} canSend={!isWaiting} />
    </div>
  );
}
