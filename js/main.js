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
        balance.innerHTML = `Баланс: ${userBalance}
