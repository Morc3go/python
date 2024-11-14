// Confirmação para deletar uma tarefa
document.addEventListener("DOMContentLoaded", function() {
    const deleteForms = document.querySelectorAll("form.delete-task");

    deleteForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            const confirmDelete = confirm("Tem certeza de que deseja deletar esta tarefa?");
            if (confirmDelete) {
                form.submit();
            }
        });
    });
});

// Validação de campos obrigatórios no formulário
function validateForm(event) {
    const titleInput = document.querySelector("input[name='title']");
    const descriptionInput = document.querySelector("textarea[name='description']");
    let valid = true;

    if (!titleInput.value.trim()) {
        alert("Por favor, insira um título para a tarefa.");
        titleInput.focus();
        valid = false;
    } else if (!descriptionInput.value.trim()) {
        alert("Por favor, insira uma descrição para a tarefa.");
        descriptionInput.focus();
        valid = false;
    }

    if (!valid) {
        event.preventDefault();
    }
}

const taskForm = document.querySelector("form.task-form");
if (taskForm) {
    taskForm.addEventListener("submit", validateForm);
}

// Auto-hide flash messages after a few seconds
function hideFlashMessages() {
    const flashMessages = document.querySelectorAll(".alert");
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.display = "none";
        }, 3000); // 3 segundos
    });
}

hideFlashMessages();

// Alternar visibilidade do menu no mobile
const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector("nav");

if (navToggle) {
    navToggle.addEventListener("click", () => {
        navLinks.classList.toggle("visible");
    });
}
