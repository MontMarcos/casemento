        // Script simples para simular a marcação de um item
        document.addEventListener('DOMContentLoaded', () => {
            const buttons = document.querySelectorAll('.status-button');
            buttons.forEach(button => {
                button.addEventListener('click', () => {
                    if (button.textContent === 'Disponível') {
                        button.textContent = 'Comprado';
                        button.classList.add('claimed');
                    } else {
                        button.textContent = 'Disponível';
                        button.classList.remove('claimed');
                    }

                    alert("🎉 Item marcado! Lembre-se que essa marcação é local no seu navegador. Por favor, entre em contato com os noivos para confirmar o presente e evitar duplicidades. Muito obrigado!");
                });
            });
        });
