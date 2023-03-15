import os

respuestas = {"Bienvenida":["Hola, soy Bella, tu Bot de ayuda ante situaciones de acoso callejero. ¿En qué puedo ayurdarte?"],
                            "Despedida": ["¡Adiós! Gracias por confiar en mi. Espero haberte ayudado"], 
                            0: "Siento mucho la situación que estás viviendo. Aquí te dejo un contacto de emergencia que quizá puedas necesitar ahora mismo:", 
                            1: """Siento mucho lo que estás contando. Aquí te dejo algunos consejos que quizá puedan ayudarte: 
- Intenta mantener la calma. 
- No respondas al/los acosador/es ni reveles información personal.
- Sigue caminando hacia un lugar público y transitado, si no lo estás ya y si es posible.  
- Pide ayuda a personas cercanas o ejecuta el comando 'ayuda' de este chat para obtener contactos a los que llamar en caso de emergencia.
Y recuerda, no estás sola, estoy aquí para ayudarte.""", 
                            2: "Para ayudarte en este momento, te dejo aquí información oficial a la que siempre podrás recurrir:"}

saludos = ['hi','hola', 'hello', 'buenos días', 'buenas tardes', 
           'buenas noches', 'cómo estás','como estas', 'tal', 'qué tal','que tal', 
           'qué hay', 'hey', 'buen día', 'buenas tardes', 'buenas noches']

despedidas = [
    "hasta pronto", "hasta la vista", "adiós", "adios", "nos vemos", "chao", "hasta luego",
    "que tengas un buen día","que te vaya bien","cuídate", "hasta la próxima",
    "buenas noches", "gracias", "muchas gracias", "chao", "ciao"]


