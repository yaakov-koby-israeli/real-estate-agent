export async function fetchProjects() {
  const response = await fetch("/api/projects");
  if (!response.ok) {
    throw new Error(`Failed to load projects (${response.status})`);
  }
  return response.json();
}
