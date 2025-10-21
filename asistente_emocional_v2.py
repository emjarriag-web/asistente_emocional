import os
import io
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment

TOKEN = os.getenv("TOKEN")

# 🔍 Detección de emoción básica (sin IA pesada)
def detectar_emocion(texto):
    texto = texto.lower()
    emociones = {
        "feliz": ["feliz", "contento", "alegre", "bien", "motivado", "positivo"],
        "triste": ["triste", "mal", "deprimido", "solo", "llorando", "cansado"],
        "enojado": ["enojado", "molesto", "furioso", "frustrado", "odio"],
        "ansioso": ["nervioso", "ansioso", "preocupado", "estresado"],
        "neutral": []
    }
    for emocion, palabras in emociones.items():
        if any(palabra in texto for palabra in palabras):
            return emocion
    return "neutral"

# 💬 Respuestas emocionales más naturales
respuestas = {
    "feliz": [
        "¡Qué alegría bro! 😄 Me encanta verte así de positivo 🔥",
        "Eso suena increíble, disfruta ese buen momento 🌞",
        "Esa energía positiva se contagia, sigue así 😎"
    ],
    "triste": [
        "Bro… lo siento 😔. A veces cuesta, pero créeme, no estarás así siempre.",
        "Entiendo que te sientas así, pero cada día puede mejorar 💪",
        "Tómate tu tiempo, respira, y recuerda que no estás solo ❤️"
    ],
    "enojado": [
        "Wow bro, suena que estás muy molesto 😤. Intenta calmarte un poco, hablarlo ayuda.",
        "Es normal enojarse, pero no dejes que eso te controle 🔥",
        "Respira un momento bro, a veces soltarlo es lo mejor 🧘‍♂️"
    ],
    "ansioso": [
        "Hey, tranquilo bro 😌. Respira profundo, no estás solo.",
        "La ansiedad no define quién eres, solo es una señal de que te importa ❤️",
        "Tú puedes manejarlo, paso a paso bro 🙏"
    ],
    "neutral": [
        "Te entiendo bro, gracias por compartirlo.",
        "Hmm interesante… ¿quieres contarme más sobre eso?",
        "Aquí estoy para escucharte bro 🤝"
    ]
}

# 🔈 Procesar texto
async def texto_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    emocion = detectar_emocion(texto)
    respuesta = random.choice(respuestas[emocion])
    await update.message.reply_text(respuesta)

# 🎧 Procesar voz
async def voz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await context.bot.get_file(update.message.voice.file_id)
        bio = io.BytesIO()
        await file.download_to_memory(out=bio)
        bio.seek(0)

        audio = AudioSegment.from_file(bio, format="ogg")
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="es-ES")

        emocion = detectar_emocion(texto)
        respuesta = random.choice(respuestas[emocion])
        await update.message.reply_text(f"Escuché: “{texto}”\n\n{respuesta}")

    except Exception as e:
        await update.message.reply_text("Hubo un error al procesar tu audio 😅")

# 🚀 Iniciar bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola bro! Soy tu asistente emocional 🤖. Cuéntame cómo te sientes o mándame una nota de voz 🎧")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_handler))
app.add_handler(MessageHandler(filters.VOICE, voz_handler))

if __name__ == "__main__":
    print("🤖 Asistente emocional mejorado corriendo...")
    app.run_polling()







