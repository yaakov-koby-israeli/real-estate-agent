import { useCallback, useEffect, useRef, useState } from "react";
import { SessionExpiredError, sendMessage, startChat } from "../../api/chatApi";
import ChatInput from "./ChatInput";
import MessageList from "./MessageList";
import OptionButtons from "./OptionButtons";
import "./ChatWidget.css";

const ERROR_TEXT = "מצטערים, משהו השתבש. נסו שוב בעוד רגע.";
const RESTART_TEXT = "השיחה התאפסה, מתחילים מחדש 🙂";

// Open/closed state lives in App, so other parts of the page (e.g. the Hero button) can open the chat.
export default function ChatWidget({ isOpen, onOpen, onClose }) {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [options, setOptions] = useState([]);
  const [step, setStep] = useState(null);
  const [isWaiting, setIsWaiting] = useState(false);
  const hasStarted = useRef(false);

  // useCallback keeps the same function between renders, so the effect below doesn't re-run for nothing.
  const addMessage = useCallback((role, text) => {
    setMessages((prev) => [...prev, { role, text }]);
  }, []);

  const applyResponse = useCallback((data) => {
    setSessionId(data.session_id);
    setStep(data.step);
    setOptions(data.options);
    addMessage("bot", data.text);
  }, [addMessage]);

  const begin = useCallback(async () => {
    setIsWaiting(true);
    try {
      applyResponse(await startChat());
    } catch {
      hasStarted.current = false; // let the next open try again
      addMessage("bot", ERROR_TEXT);
    } finally {
      setIsWaiting(false);
    }
  }, [addMessage, applyResponse]);

  // Start the conversation the first time the chat is opened - no matter who opened it.
  useEffect(() => {
    if (isOpen && !hasStarted.current) {
      hasStarted.current = true;
      begin();
    }
  }, [isOpen, begin]);

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
      <button className="chat-launcher" onClick={onOpen} aria-label="פתיחת צ'אט עם הסוכן הווירטואלי">
        💬
      </button>
    );
  }

  const isDone = step === "done";

  return (
    <div className="chat">
      <div className="chat__header">
        <span>הסוכן הווירטואלי של פרשקובסקי</span>
        <button className="chat__close" onClick={onClose} aria-label="סגירה">✕</button>
      </div>
      <MessageList messages={messages} isTyping={isWaiting} />
      <OptionButtons options={options} onSelect={send} disabled={isWaiting} />
      <ChatInput onSend={send} disabled={isDone || !sessionId} canSend={!isWaiting} />
    </div>
  );
}
