### Resumidor Estatal
bot de reddit para resumir noticias

Fusión de [u/empleadoEstatalBot](https://github.com/andreskrey/empleadoEstatalBot) y [TextRank (de Summa NLP)](https://github.com/summanlp/textrank)

El flow es bastante sencillo:
* Monitorea los comentarios de un usuario en particular (u/empleadoEstatalBot en este caso)
* Agarra los últimos n comentarios del usuario
* Filtra de esos n comentarios para quedarse solo con los que sean dentro de los subreddits permitidos y que tenga mas de x palabras (no tiene sentido resumir una noticia de menos de 100 palabras, por ejemplo)
* Recorre todas las respuestas del comentario seleccionado. Si alguna es el mismo bot, entonces ya esta respondido. Si no, entonces queda por responder.
* Con TextRank se responde el comentario original con un resumen de su texto
* Se duerme el bot 1 minuto, y luego vuelve a empezar todo el loop.

---

## Como correrlo local

Crear un usuario para usar de bot y obtener las credenciales de PRAW (registrando una aplicación de reddit). También se puede crear un subreddit para usar de pruebas (o usar [r/test](reddit.com/r/test))

```
# Instalar las dependencias
$ pip install -r requirements.txt

# Configurar las variables de entorno con las credenciales y demás
$ export CLIENT_ID="xxx"
$ export CLIENT_SECRET="xxx"
$ export USER_AGENT="xxx"
$ export BOT_USERNAME="xxx"
$ export BOT_PASSWORD="xxx"

# Configurar el resto de las variables de entorno
$ export REPLY_TO="botdummy" # El usuario que se monitorea
$ export SUBREDDITS="test botplayground" # Lista de subreddits (separada por espacios) donde se comenta
$ export ME="bot" # El bot configurado
$ export LOGLEVEL="INFO" # Mensajes de INFO o DEBUG
```

En [config.py](config.py) se pueden cambiar algunos parametros del comportamiento del programa.

```
python resumidor_estatal.py
```

---

## Donde esta servido

[Heroku](https://heroku.com/)!
