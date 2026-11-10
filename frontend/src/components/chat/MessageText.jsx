// Turns the agent's light markdown into React elements - safely, without dangerouslySetInnerHTML.
// React escapes every string we render, and only http(s) URLs ever become links.

// [label](https://...)  |  **bold**  |  https://...
const TOKEN_PATTERN = /(\[[^\]]+\]\(https?:\/\/[^)\s]+\)|\*\*[^*]+\*\*|https?:\/\/[^\s)]+)/g;
const MARKDOWN_LINK = /^\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)$/;
const DEFAULT_LINK_LABEL = "לפרטי הפרויקט ←";

function Link({ href, children }) {
  return (
    <a href={href} target="_blank" rel="noreferrer" className="chat__link">
      {children}
    </a>
  );
}

function renderToken(token, index) {
  const markdownLink = token.match(MARKDOWN_LINK);
  if (markdownLink) {
    return <Link key={index} href={markdownLink[2]}>{markdownLink[1]}</Link>;
  }
  if (token.startsWith("**") && token.endsWith("**")) {
    return <strong key={index}>{token.slice(2, -2)}</strong>;
  }
  if (token.startsWith("http")) {
    const href = token.replace(/[.,]+$/, ""); // a sentence's final period is not part of the URL
    return <Link key={index} href={href}>{DEFAULT_LINK_LABEL}</Link>;
  }
  return token;
}

export default function MessageText({ text }) {
  return text.split(TOKEN_PATTERN).map(renderToken);
}
