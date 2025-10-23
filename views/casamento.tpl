<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Presentes - Breno e Danyella</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../static/css/mobile.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    
    </head>
<body>
    
    <header>
        <h1>BRENO</h1>
        <h1>E</h1>
        <h1>DANYELLA</h1>
        <h2 class="subtitle">NOSSA LISTA DE CHÁ DE PANELA</h2>
    </header>

    <div class="container">
        <h3>Com Carinho, Para o Novo Lar!</h3>
        <p class="intro-text">Estamos muito felizes em celebrar este momento especial com vocês! Sua presença já é o maior presente, mas se quiserem nos ajudar a montar nossa casinha, aqui está uma lista do que precisamos.</p>
        <p class="intro-text">Ao escolher um item, por favor, clique em Comprar para marcá-lo como indisponível e evitar duplicidades.</p>
        <p> Cores inox, preto ou branco</p>
        
        <ul class="gift-list">
            {% for item in lista_itens %}
            <li class="{% if item.comprado %}claimed{% endif %}">
                <span class="item-name">{{ item.nome }}</span> 
                
                {% if item.comprado %}
                    <button class="btn-desativado" disabled>Irão presentiar</button>
                {% else %}
                    <form method="POST" action="{{ url_for('comprar') }}">
                        <input type="hidden" name="gift_id" value="{{ item.id }}">
                        <button type="submit" class="btn-comprar">
                            Comprar
                        </button>
                    </form>
                    
                    {% endif %}
            </li>
            {% endfor %}
        </ul>
    </div>

    <footer>
        <p>Agradecemos de coração! Com amor, Breno e Danyella.</p>
    </footer>

   <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>