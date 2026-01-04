from django.shortcuts import render, HttpResponse

def home(request):
    # Используем f-строку или обычные тройные кавычки для многострочного текста
    html_content = """
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <style>
            body { font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; }
            .login-container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Sign-in</h2>
            <form method="POST">
                <input type="email" name="email" placeholder="Email" required><br><br>
                <input type="password" name="password" placeholder="Password" required><br><br>
                <button type="submit">Lock in</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)