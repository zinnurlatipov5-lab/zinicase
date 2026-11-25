document.addEventListener('DOMContentLoaded', () => {
    const caseResult = document.getElementById('case-result');
    const balance = document.getElementById('balance');
    let userBalance = 0;

    const prizes = {
        'common': ['Обычный подарок', 'Снежная шапка', 'Ёлочный шар'],
        'rare': ['Редкий подарок', 'Тёплая варежка', 'Новогодний фонарик'],
        'legendary': ['Легендарный подарок', 'Снежный трон', 'Хрустальная снежинка']
    };

    async function openCase(category) {
        if (userBalance >= 10) {
            const prize = prizes[category][Math.floor(Math.random() * prizes[category].length)];
            caseResult.innerHTML = `Вы открыли: ${prize}`;
            userBalance -= 10;
            balance.innerHTML = `Баланс: ${userBalance} звёзд`;
        } else {
            alert('Недостаточно звёзд!');
        }
    }

    function inviteFriends() {
        alert('Пригласите 3 друзей и получите шанс на бесплатный кейс!');
    }

      function checkBalance() {
        balance.innerHTML = `Баланс: ${userBalance} звёзд`;
    }

    checkBalance();

    // Функция для открытия кейса с оплатой
    async function buyCase(category) {
        if (confirm('Купить кейс за 10 звёзд?')) {
            userBalance -= 10;
            balance.innerHTML = `Баланс: ${userBalance} звёзд`;
            
            // Здесь должна быть логика интеграции с ЮKassa
            // Для примера используем alert
            alert('Оплата успешна! Открываем кейс...');
            
            const prize = prizes[category][Math.floor(Math.random() * prizes[category].length)];
            caseResult.innerHTML = `Вы открыли: ${prize}`;
        }
    }

    // Обработка приглашения друзей
    function inviteFriends() {
        alert('Пригласите 3 друзей и получите шанс на бесплатный кейс!');
    }

    // События кнопок
    document.querySelectorAll('.cases button').forEach(button => {
        button.addEventListener('click', () => {
            const category = button.textContent.trim();
            if (category === 'Обычный') {
                buyCase('common');
            } else if (category === 'Редкий') {
                buyCase('rare');
            } else if (category === 'Легендарный') {
                buyCase('legendary');
            }
        });
    });
});
