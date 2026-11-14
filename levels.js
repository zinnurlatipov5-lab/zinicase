// ===== Ёлка Зини: таблица 100 уровней =====
// Опыт до следующего уровня: 200 * уровень^1.5
// Итого до 100 уровня — около 8 млн опыта (месяцы игры, первые уровни быстрые)

var XP_TABLE = [];
(function () {
  for (var i = 1; i <= 100; i++) {
    XP_TABLE.push(Math.round(200 * Math.pow(i, 1.5)));
  }
})();

function xpToNext(level) {
  return XP_TABLE[Math.min(level - 1, 99)] || 400;
}
