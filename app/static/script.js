// Confirmação para deletar uma tarefa
document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os formulários com a classe 'delete-task'
    const deleteForms = document.querySelectorAll("form.delete-task");

    // Adiciona um ouvinte de evento para cada formulário de exclusão
    deleteForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            // Impede o envio do formulário imediatamente
            event.preventDefault();

            // Exibe uma janela de confirmação antes de excluir
            const confirmDelete = confirm("Tem certeza de que deseja deletar esta tarefa?");
            if (confirmDelete) {
                // Se o usuário confirmar, o formulário será enviado
                form.submit();
            }
        });
    });
});

// Validação de campos obrigatórios no formulário de criação ou edição de tarefa
function validateForm(event) {
    // Seleciona os campos do formulário para título e descrição
    const titleInput = document.querySelector("input[name='title']");
    const descriptionInput = document.querySelector("textarea[name='description']");
    let valid = true;

    // Verifica se o título foi preenchido
    if (!titleInput.value.trim()) {
        alert("Por favor, insira um título para a tarefa.");
        titleInput.focus(); // Foca no campo de título
        valid = false;
    } else if (!descriptionInput.value.trim()) { // Verifica se a descrição foi preenchida
        alert("Por favor, insira uma descrição para a tarefa.");
        descriptionInput.focus(); // Foca no campo de descrição
        valid = false;
    }

    // Se algum campo não for válido, impede o envio do formulário
    if (!valid) {
        event.preventDefault();
    }
}

// Seleciona o formulário de tarefas
const taskForm = document.querySelector("form.task-form");
if (taskForm) {
    // Adiciona o ouvinte de evento de validação ao formulário de tarefas
    taskForm.addEventListener("submit", validateForm);
}

// Função para esconder mensagens flash após alguns segundos
function hideFlashMessages() {
    // Seleciona todas as mensagens de alerta com a classe 'alert'
    const flashMessages = document.querySelectorAll(".alert");
    flashMessages.forEach(message => {
        // Define um tempo de 3 segundos para esconder cada mensagem
        setTimeout(() => {
            message.style.display = "none";
        }, 3000); // 3 segundos
    });
}

// Chama a função para esconder mensagens flash assim que a página carregar
hideFlashMessages();

// Alternar visibilidade do menu de navegação no mobile
const navToggle = document.querySelector(".nav-toggle"); // Botão que ativa/desativa o menu
const navLinks = document.querySelector("nav"); // O menu de navegação em si

// Verifica se o botão de alternância de menu existe
if (navToggle) {
    // Adiciona um ouvinte de evento de clique para alternar a visibilidade do menu
    navToggle.addEventListener("click", () => {
        navLinks.classList.toggle("visible"); // Adiciona ou remove a classe 'visible' no menu
    });
}
