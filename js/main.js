document.addEventListener('DOMContentLoaded', () => {
    const caseResult = document.getElementById('case-result');
    const balance = document.getElementById('balance');

    let userBalance = 0;

    async function openFreeCase() {
        if (userBalance >= 0) {
            const prize = getRandomPrize();
            caseResult.innerHTML = `Вы открыли: ${prize}`;
            userBalance--; // Уменьшаем баланс после открытия
            balance.innerHTML = `Баланс: ${userBalance} звёзд`;
        } else {
            alert('Необходимо пригласить 3 друзей для бесплатного кейса!');
        }
    }

    function buyCase() {
        if (confirm('Купить кейс за 10 звёзд?')) {
            userBalance -= 10;
            balance.innerHTML = `Баланс: ${userBalance} звёзд`;
            getPaidPrize();
        }
    }

    function getPaidPrize() {
        const prize = ['Обычный подарок', 'Редкий подарок', 'Эксклюзивный подарок'][Math.floor(Math.random() * 3)];
        caseResult.innerHTML = `Вы получили: ${prize}`;
    }

    function inviteFriends() {
        alert('Пригласите 3 друзей и получите шанс на бесплатный кейс!');
    }

    function checkBalance() {
        balance.innerHTML = `Баланс: ${userBalance} звёзд`;
    }

    checkBalance();
