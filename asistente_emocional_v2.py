import os
import io
import random
from textblob import TextBlob
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment

TOKEN = os.getenv("TOKEN")  # tu token de Telegram (debe estar en Render o .env)

# Análisis de sentimiento
def analizar_sentimiento(texto):
    analisis = TextBlob(texto).sentiment.polarity
    if analisis > 0.1:
        return "positivo"
    elif analisis < -0.1:
        return "negativo"
    else:
        return "neutro"

# Respuestas emocionales
mensajes = {
    "positivo": [
        "¡Me alegra escuchar eso, bro! 😄",
        "¡Esa es la actitud, sigue así 🔥!",
        "Qué buena vibra transmites hoy 😎"
    ],
    "negativo": [
        "Hey bro, tranquilo... todo mejora, te lo prometo 💪",
        "A veces los días duelen, pero no duran para siempre 🖤",
        "Cuenta conmigo bro, estoy aquí contigo 🤝"
    ],
    "neutro": [
        "Entiendo lo que dices, bro.",
        "Hmm interesante 😶",
        "¿Quieres contarme más sobre eso?"
    ]
}

# Mensaje de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola bro! Soy tu asistente emocional 🤖. Puedes hablarme o mandarme una nota de voz 💬🎧")

# Cuando el usuario manda texto
async def texto_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    estado = analizar_sentimiento(texto)
    respuesta = random.choice(mensajes[estado])
    await update.message.reply_text(respuesta)

# Cuando el usuario manda audio
async def voz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await context.bot.get_file(update.message.voice.file_id)
        bio = io.BytesIO()
        await file.download_to_memory(out=bio)
        bio.seek(0)

        # Convertir OGG a WAV sin usar ffmpeg.exe
        audio = AudioSegment.from_file(bio, format="ogg")
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="es-ES")

        estado = analizar_sentimiento(texto)
        respuesta = random.choice(mensajes[estado])
        await update.message.reply_text(f"Escuché: “{texto}”\n\n{respuesta}")

    except Exception as e:
        await update.message.reply_text(f"Hubo un error al procesar tu audio 😅 ({e})")

# Iniciar el bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_handler))
app.add_handler(MessageHandler(filters.VOICE, voz_handler))

if __name__ == "__main__":
    print("🤖 Asistente emocional corriendo...")
    app.run_polling()






