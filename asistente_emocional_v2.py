import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from textblob import TextBlob
import random
from pydub import AudioSegment
import io
import speech_recognition as sr

# Token del bot (usa variable de entorno en Render)
TOKEN = os.environ.get("TOKEN")

# Mensajes motivacionales más largos
mensajes = {
    "positivo": [
        "¡Me alegra que te sientas así! Sigue así 😎. Recuerda que cada día es una oportunidad para crecer y hacer cosas increíbles.",
        "Genial, eso es energía positiva 💪. Mantén esa actitud y verás que todo mejora aún más.",
        "Sigue disfrutando de tu día, bro 🌟. Cada pequeño logro cuenta y estoy aquí para celebrarlo contigo."
    ],
    "negativo": [
        "Ánimo, esto va a mejorar 😌. A veces las cosas se ponen difíciles, pero todo tiene solución y no estás solo.",
        "Recuerda que después de la lluvia siempre sale el sol ☀️. Respira profundo y vamos paso a paso.",
        "Tranquilo, bro, todo tiene solución 💪. No dejes que un mal momento defina tu día, ¡tú puedes con esto!"
    ],
    "neutral": [
        "Entiendo, gracias por compartirlo 😊. A veces solo necesitamos expresar cómo nos sentimos para seguir adelante.",
        "Gracias por contarme, bro. Estoy aquí para escucharte y acompañarte en lo que necesites.",
        "Todo bien, seguimos adelante 😎. Cada día es una nueva oportunidad para mejorar y aprender algo nuevo."
    ]
}

# Analizar sentimiento del texto
def analizar_sentimiento(texto):
    polaridad = TextBlob(texto).sentiment.polarity
    if polaridad > 0.1:
        return "positivo"
    elif polaridad < -0.1:
        return "negativo"
    else:
        return "neutral"

# Función para responder mensajes de texto
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    estado = analizar_sentimiento(texto)
    respuesta = random.choice(mensajes[estado])
    await update.message.reply_text(respuesta)

# Función para procesar voice messages de Telegram
async def procesar_voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Descargar archivo de voz de Telegram
    file = await context.bot.get_file(update.message.voice.file_id)
    bio = io.BytesIO()
    await file.download(out=bio)
    bio.seek(0)
    
    # Convertir OGG a WAV
    audio = AudioSegment.from_ogg(bio)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    
    # Reconocer texto
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio_data, language="es-ES")
        except:
            texto = None
    
    if texto:
        estado = analizar_sentimiento(texto)
        respuesta = random.choice(mensajes[estado])
        await update.message.reply_text(respuesta)
    else:
        await update.message.reply_text("No entendí bro 😅, intenta de nuevo.")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola bro! Soy tu asistente Emocional 😎. "
        "Cuéntame cómo te sientes o mándame un mensaje de voz."
    )

# Crear bot y handlers
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.add_handler(MessageHandler(filters.VOICE, procesar_voz))

print("asistente emocional activo... 🚀")
app.run_polling()


