<script>
    const width = window.innerWidth;
    const height = window.innerHeight;

    const isMobile = width <= 576;

    // Сообщение
    const message = isMobile
        ? `📱 Мобильное устройство\nРазрешение: ${width}x${height}`
        : `💻 Компьютер\nРазрешение: ${width}x${height}`;

    // 1. Вывод в консоль

    console.log(message);

    // 2. Alert на экране
    alert(message);

    // 3. Отображение на странице
    document.addEventListener("DOMContentLoaded", function () {
        const div = document.createElement("div");
        div.style.padding = "10px";
        div.style.backgroundColor = "#f8f9fa";
        div.style.border = "1px solid #ccc";
        div.style.fontSize = "16px";
        div.style.fontFamily = "Arial, sans-serif";
        div.innerText = message;
        document.body.prepend(div);

    });
</script>
