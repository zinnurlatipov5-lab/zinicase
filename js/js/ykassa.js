async function ykassaPayment(amount, callbackSuccess, callbackError) {
    // Здесь должна быть логика интеграции с ЮKassa
    // Пример: отправка данных на сервер для обработки платежа
    // Для простоты используем alert
    alert(`Производим оплату ${amount} звёзд`);
    
    // Пример успешного завершения
    if (amount >= 10) {
        callbackSuccess(amount);
    } else {
        callbackError('Недостаточно средств');
    }
}

function getPaidPrize() {
    ykassaPayment(10, (amount) => {
        console.log('Оплата успешна, получаем приз');
        // Здесь логика получения приза
    }, (error) => {
        console.error('Ошибка оплаты:', error);
    });
}
