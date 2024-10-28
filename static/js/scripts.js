function buyStock(stockCode, price) {
    fetch('/api/save_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ stockCode, price, action: 'buy' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('股票購買成功！');
            window.location.reload();
        } else {
            alert('購買股票時出錯，請重試。');
        }
    });
}

function sellStock(stockCode) {
    fetch('/api/save_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ stockCode, action: 'sell' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('股票賣出成功！');
            window.location.reload();
        } else {
            alert('賣出股票時出錯，請重試。');
        }
    });
}

function sellAllStocks() {
    fetch('/api/save_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'sell_all' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('所有股票已賣出！');
            window.location.reload();
        } else {
            alert('賣出股票時出錯，請重試。');
        }
    });
}
