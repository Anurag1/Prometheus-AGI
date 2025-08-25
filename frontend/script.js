document.addEventListener('DOMContentLoaded', () => {
    const projectListEl = document.getElementById('projectList');
    const newProjectBtn = document.getElementById('newProjectBtn');
    const modal = document.getElementById('newProjectModal');
    const closeModal = document.querySelector('.close-button');
    const newProjectForm = document.getElementById('newProjectForm');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const projectDetail = document.getElementById('projectDetail');
    const runAgentBtn = document.getElementById('runAgentBtn');
    
    let currentProject = null;

    async function loadProjects() {
        const response = await fetch('/api/projects');
        const projects = await response.json();
        projectListEl.innerHTML = '';
        projects.forEach(name => {
            const div = document.createElement('div');
            div.className = 'project-item';
            div.textContent = name;
            div.onclick = () => viewProject(name);
            projectListEl.appendChild(div);
        });
    }

    async function viewProject(name) {
        currentProject = { name };
        const response = await fetch(`/api/projects/${name}`);
        const data = await response.json();

        // Use localStorage to remember the goal for each project
        const storedGoal = localStorage.getItem(`project-goal-${name}`);
        if (storedGoal) {
            currentProject.goal = storedGoal;
        } else {
            const goal = prompt(`This seems to be the first time opening this project. Please provide its goal:`);
            if (goal) {
                currentProject.goal = goal;
                localStorage.setItem(`project-goal-${name}`, goal);
            } else return; // User cancelled
        }
        
        document.querySelectorAll('.project-item').forEach(el => el.classList.remove('active'));
        [...document.querySelectorAll('.project-item')].find(el => el.textContent === name).classList.add('active');

        document.getElementById('projectName').textContent = name;
        document.getElementById('projectGoal').textContent = `Goal: ${currentProject.goal}`;
        document.getElementById('projectHypotheses').textContent = JSON.stringify(data.hypotheses || 'No hypotheses yet.', null, 2);
        document.getElementById('projectState').textContent = JSON.stringify(data.latest_state || 'No state recorded yet.', null, 2);
        
        welcomeScreen.style.display = 'none';
        projectDetail.style.display = 'block';
    }

    runAgentBtn.addEventListener('click', async () => {
        if (!currentProject) return;
        alert(`Triggering agent for project: ${currentProject.name}. Check terminal logs for progress. Refresh this page in a few minutes to see results.`);
        runAgentBtn.textContent = "Agent is Running...";
        runAgentBtn.disabled = true;
        
        await fetch(`/api/projects/${currentProject.name}/run`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(currentProject)
        });
        
        setTimeout(() => {
            runAgentBtn.textContent = "Run Agent";
            runAgentBtn.disabled = false;
        }, 10000); // Re-enable button after 10 seconds
    });

    newProjectBtn.onclick = () => modal.style.display = 'block';
    closeModal.onclick = () => modal.style.display = 'none';
    newProjectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('newProjectName').value;
        const goal = document.getElementById('newProjectGoal').value;
        await fetch('/api/projects', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name, goal })
        });
        localStorage.setItem(`project-goal-${name}`, goal);
        modal.style.display = 'none';
        newProjectForm.reset();
        await loadProjects();
        await viewProject(name);
    });

    loadProjects();
});