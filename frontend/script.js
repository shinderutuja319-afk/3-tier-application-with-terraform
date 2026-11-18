const taskInput = document.getElementById("taskInput");
const addButton = document.getElementById("addButton");
const taskList = document.getElementById("taskList");
const message = document.getElementById("message");

async function apiRequest(url, options = {}) {
    const response = await fetch(url, options);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
    }

    return data;
}

async function loadTasks() {
    try {
        const tasks = await apiRequest("/api/tasks");

        taskList.replaceChildren();

        if (tasks.length === 0) {
            taskList.textContent = "No tasks yet. Add your first task!";
            return;
        }

        tasks.forEach(task => {
            const item = document.createElement("div");
            item.className = "task-item";

            if (task.completed) {
                item.classList.add("completed");
            }

            const title = document.createElement("span");
            title.textContent = task.title;

            const actions = document.createElement("div");
            actions.className = "task-actions";

            const toggle = document.createElement("button");
            toggle.textContent = task.completed ? "Undo" : "Done";

            toggle.addEventListener("click", async () => {
                try {
                    await apiRequest(`/api/tasks/${task.id}`, {
                        method: "PATCH",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            completed: !task.completed
                        })
                    });

                    loadTasks();
                } catch (error) {
                    message.textContent = error.message;
                }
            });

            const remove = document.createElement("button");
            remove.textContent = "Delete";
            remove.className = "delete-button";

            remove.addEventListener("click", async () => {
                try {
                    await apiRequest(`/api/tasks/${task.id}`, {
                        method: "DELETE"
                    });

                    loadTasks();
                } catch (error) {
                    message.textContent = error.message;
                }
            });

            actions.append(toggle, remove);
            item.append(title, actions);
            taskList.appendChild(item);
        });

    } catch (error) {
        taskList.textContent = "Unable to load tasks.";
        message.textContent = error.message;
    }
}

async function addTask() {
    const title = taskInput.value.trim();

    if (!title) {
        message.textContent = "Please enter a task.";
        return;
    }

    try {
        await apiRequest("/api/tasks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title})
        });

        taskInput.value = "";
        message.textContent = "";
        loadTasks();

    } catch (error) {
        message.textContent = error.message;
    }
}

addButton.addEventListener("click", addTask);

taskInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        addTask();
    }
});

loadTasks();