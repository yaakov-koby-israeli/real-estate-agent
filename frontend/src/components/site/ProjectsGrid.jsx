import { useEffect, useState } from "react";
import { fetchProjects } from "../../api/projectsApi";
import ProjectCard from "./ProjectCard";
import "./ProjectsGrid.css";

const FILTERS = [
  { value: "all", label: "כל הפרויקטים" },
  { value: "residential", label: "מגורים" },
  { value: "urban_renewal", label: "התחדשות עירונית" },
  { value: "rental", label: "דיור להשכרה" },
];

export default function ProjectsGrid() {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch(setError)
      .finally(() => setIsLoading(false));
  }, []);

  const visibleProjects =
    filter === "all" ? projects : projects.filter((p) => p.categories.includes(filter));

  return (
    <section id="projects" className="projects">
      <div className="container">
        <h2 className="projects__title">הפרויקטים שלנו</h2>

        <div className="projects__filters">
          {FILTERS.map((f) => (
            <button
              key={f.value}
              className={`projects__filter ${filter === f.value ? "projects__filter--active" : ""}`}
              onClick={() => setFilter(f.value)}
            >
              {f.label}
            </button>
          ))}
        </div>

        {isLoading && <p className="projects__message">טוען פרויקטים...</p>}
        {error && <p className="projects__message projects__message--error">לא הצלחנו לטעון את הפרויקטים. נסו שוב מאוחר יותר.</p>}

        <div className="projects__grid">
          {visibleProjects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
    </section>
  );
}
