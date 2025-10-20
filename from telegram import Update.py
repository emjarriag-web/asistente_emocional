from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from textblob import TextBlob
import pyttsx3
import random

# Configurar voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # velocidad de la voz

# Mensajes motivacionales
mensajes = {
    "positivo": [
        "¡Me alegra que te sientas así! Sigue así 😎",
        "Genial, eso es energía positiva 💪",
        "Sigue disfrutando de tu día, bro 🌟"
    ],
    "negativo": [
        "Ánimo, esto va a mejorar 😌",
        "Recuerda que después de la lluvia siempre sale el sol ☀️",
        "Tranquilo, bro, todo tiene solución 💪"
    ],
    "neutral": [
        "Entiendo, gracias por compartirlo 😊",
        "Gracias por contarme, bro",
        "Todo bien, seguimos adelante 😎"
    ]
}

# Analizar sentimiento
def analizar_sentimiento(texto):
    polaridad = TextBlob(texto).sentiment.polarity
    if polaridad > 0.1:
        return "positivo"
    elif polaridad < -0.1:
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
    
    # Respuesta por voz en tu PC
    engine.say(respuesta)
    engine.runAndWait()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bro! Soy tu asistente Emocional 😎. Cuéntame cómo te sientes.")

# Token de tu bot (pon el que te dio BotFather)
TOKEN = "TU_TOKEN_AQUI"

# Crear bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("asistente emocional activo... 🚀")
app.run_polling()
