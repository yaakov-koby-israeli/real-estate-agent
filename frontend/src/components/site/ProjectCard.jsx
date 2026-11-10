import "./ProjectCard.css";

const STATUS_LABELS = {
  marketing: "בשיווק",
  future: "עתידי",
  populated: "מאוכלס",
};

export default function ProjectCard({ project }) {
  return (
    <a className="project-card" href={project.url} target="_blank" rel="noreferrer">
      <div className="project-card__image">
        {project.image_url && <img src={project.image_url} alt={project.name} loading="lazy" />}
        {project.status && (
          <span className={`project-card__status project-card__status--${project.status}`}>
            {STATUS_LABELS[project.status]}
          </span>
        )}
      </div>
      <div className="project-card__body">
        <h3 className="project-card__name">{project.name}</h3>
        {project.city && <p className="project-card__city">{project.city}</p>}
      </div>
    </a>
  );
}
