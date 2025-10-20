import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from textblob import TextBlob
import random

# Token del bot desde variable de entorno
TOKEN = os.environ.get("TOKEN")

# Mensajes motivacionales épicos
mensajes = {
    "positivo": [
        "¡Wow bro! Me encanta ver que estás con tanta energía positiva 😎. Sigue así y contagia esa buena vibra a todos los que te rodean 💯",
        "Genial, bro! Tu actitud positiva es increíble. Cada paso que das te acerca más a tus metas, ¡sigue adelante! 💪",
        "Increíble bro, mantener esta motivación no es fácil, pero tú lo logras. Recuerda celebrar cada pequeño logro 🌟",
        "Tu energía es contagiosa, bro. Mantén esa buena vibra y sigue creciendo en lo que te apasiona 😄",
        "Sigue así, bro. Cada día que aprovechas positivamente es un paso gigante hacia tu mejor versión 🚀"
    ],
    "negativo": [
        "Sé que estás pasando por un momento difícil, bro. Respira profundo, tomate un momento y recuerda: esto también pasará 🌈",
        "No estás solo, bro. Está bien sentirse mal a veces. Trata de hacer algo que te haga sentir mejor, aunque sea pequeño 💪",
        "Ánimo, bro. Todos tenemos días difíciles. Haz algo que te relaje o habla con alguien de confianza, verás que mejora 😌",
        "Es normal sentirse desanimado a veces. Recuerda bro: cada pequeño esfuerzo cuenta y mañana es otra oportunidad para avanzar 🌟",
        "Bro, está bien no estar bien. Escucha tu corazón, tomate un descanso si lo necesitas, y sigue adelante poco a poco 💯",
        "Si te sientes mal, intenta hacer algo que te guste o salir a caminar un momento. A veces, pequeños cambios hacen grandes diferencias 🌿"
    ],
    "neutral": [
        "Gracias por contarme cómo te sientes, bro. Está bien sentirse así a veces, seguimos adelante 😎",
        "Entiendo, bro. Cada día es una nueva oportunidad, incluso cuando todo parece normal 🌟",
        "Bro, lo que sientes es válido. Gracias por compartirlo conmigo 😊",
        "Todo bien, bro. Recuerda que estoy aquí para escucharte siempre que lo necesites 💪",
        "Gracias por abrirte, bro. A veces compartir lo que sentimos hace toda la diferencia 💯",
        "Está bien sentirse neutro, bro. Mantén la calma y sigue con tu día con tranquilidad 😌"
    ]
}

# Función mejorada de análisis de sentimiento
def analizar_sentimiento(texto):
    texto_lower = texto.lower()
    # Palabras clave negativas
    palabras_negativas = ["mal", "triste", "deprimido", "angustiado", "cansado", "desanimado", "estresado", "agotado"]
    if any(palabra in texto_lower for palabra in palabras_negativas):
        return "negativo"

    # Análisis automático con TextBlob
    polaridad = TextBlob(texto).sentiment.polarity
    if polaridad > 0.05:
        return "positivo"
    elif polaridad < 0.0:
        return "negativo"
    else:
        return "neutral"

# Función principal del bot
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    estado = analizar_sentimiento(texto)
    respuesta = random.choice(mensajes[estado])
    
    # Respuesta en Telegram
    await update.message.reply_text(respuesta)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bro! Soy tu asistente Emocional 😎. Cuéntame cómo te sientes y te daré un consejo o motivación.")

# Crear bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Asistente emocional épico activo... 🚀")
app.run_polling()


