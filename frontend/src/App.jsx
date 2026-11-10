import { useState } from "react";
import ChatWidget from "./components/chat/ChatWidget";
import Footer from "./components/site/Footer";
import Header from "./components/site/Header";
import Hero from "./components/site/Hero";
import ProjectsGrid from "./components/site/ProjectsGrid";

export default function App() {
  // Lifted up here so both Hero and ChatWidget can use it.
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <>
      <Header />
      <main>
        <Hero onOpenChat={() => setIsChatOpen(true)} />
        <ProjectsGrid />
      </main>
      <Footer />
      <ChatWidget
        isOpen={isChatOpen}
        onOpen={() => setIsChatOpen(true)}
        onClose={() => setIsChatOpen(false)}
      />
    </>
  );
}
