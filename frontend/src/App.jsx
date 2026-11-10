import Footer from "./components/site/Footer";
import Header from "./components/site/Header";
import Hero from "./components/site/Hero";
import ProjectsGrid from "./components/site/ProjectsGrid";

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <ProjectsGrid />
      </main>
      <Footer />
    </>
  );
}
