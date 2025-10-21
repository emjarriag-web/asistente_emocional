import os
import io
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pydub import AudioSegment
import speech_recognition as sr

# Tu token de Telegram desde Render (Environment Variables)
TOKEN = os.environ.get("TOKEN")

# Mensajes motivacionales
mensajes = {
    "positivo": [
        "¡Me alegra que te sientas así! Sigue así 😎 Recuerda que tu energía positiva atrae cosas buenas.",
        "Genial, eso es energía positiva 💪 Mantén tu motivación y sigue disfrutando cada momento.",
        "Sigue disfrutando de tu día, bro 🌟 La actitud positiva es contagiosa, ¡difúndela!"
    ],
    "negativo": [
        "Ánimo, esto va a mejorar 😌 Cada día es una nueva oportunidad para sentirte mejor.",
        "Recuerda que después de la lluvia siempre sale el sol ☀️ Todo tiene solución, bro, confía en ti.",
        "Tranquilo, bro, todo tiene solución 💪 Respira hondo y da un paso a la vez, no estás solo."
    ],
    "neutral": [
        "Entiendo, gracias por compartirlo 😊 Sigue así y verás cómo tu día mejora poco a poco.",
        "Gracias por contarme, bro. A veces solo expresar lo que sentimos ya ayuda bastante.",
        "Todo bien, seguimos adelante 😎 Mantén la calma y avanza paso a paso, bro."
    ]
}

# Analizar sentimiento
def analizar_sentimiento(texto):
    from textblob import TextBlob
    polaridad = TextBlob(texto).sentiment.polarity
    if polaridad > 0.1:
        return "positivo"
    elif polaridad < -0.1:
        return "negativo"
    else:
        return "neutral"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bro! Soy tu asistente emocional 😎. Envíame un voice message y te responderé según cómo te sientas.")

# Función para procesar voice messages
async def procesar_voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
    except Exception as e:
        await update.message.reply_text(f"Hubo un error al procesar tu mensaje 😓: {e}")

# Crear bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, procesar_voz))

print("Asistente emocional activo 🚀")
app.run_polling()



