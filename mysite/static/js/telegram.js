// <script>
    try {
        // Проверка: если устройство — не компьютер
        const isDesktop = /Win32|Win64|MacIntel|Linux x86_64/.test(navigator.userAgent);

        if (!isDesktop) {
            const initData = window.Telegram?.WebApp?.initData;
            const initDataUnsafe = window.Telegram?.WebApp?.initDataUnsafe;

            const userDataDiv = document.getElementById('userData');

            if (initData && initData.length > 0) {
                userDataDiv.textContent = JSON.stringify(initDataUnsafe, null, 4);

                // Автоматически отправляем initData на сервер
                fetch('/api/save-user/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        initData: initData
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Ответ сервера:', data);
                })
                .catch(error => console.error('Ошибка при отправке данных на сервер:', error));
            } else {
                userDataDiv.innerHTML = '<span style="color:red;">Страница открыта вне Telegram. Данные недоступны.</span>';
            }
        } else {
            console.log('Код не выполняется на десктопе');
        }
    } catch (error) {
        console.error('Произошла ошибка в Telegram WebApp инициализации:', error);
    }
//</script>
