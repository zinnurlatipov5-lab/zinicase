document.addEventListener('DOMContentLoaded', () => {
    const caseResult = document.getElementById('case-result');

    // Функция открытия бесплатного кейса
    async function openCase() {
        // Логика приглашения друзей (можно добавить через API)
        if (canOpenFreeCase()) {
            const prize = getRandomPrize();
            caseResult.innerHTML = `Вы открыли: ${prize}`;
            // Здесь можно добавить логику приглашения друзей
        } else {
            alert('Пригласите 3 друзей, чтобы открыть бесплатный кейс!');
        }
    }

    // Функция покупки кейса
    function buyCase() {
        // Здесь логика покупки через ЮKassa
        // После успешной оплаты вызываем функцию получения приза
        getPaidPrize();
    }

    // Функция получения случайного приза
    function getRandomPrize() {
        return ['Обычный подарок', 'Редкий подарок', 'Эксклюзивный подарок'][Math.floor(Math.random() * 3)];
    }

    // Проверка условий для бесплатного кейса
    function canOpenFreeCase() {
        // Здесь можно добавить проверку количества приглашённых друзей
        return true; // Пример проверки
    }

    // Функция получения приза после оплаты
    function getPaidPrize() {
        // Здесь можно добавить логику получения приза после оплаты
        alert('Вы получили приз после оплаты!');
    }
});
