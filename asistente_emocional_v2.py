import os
import random
import pyttsx3
import speech_recognition as sr
from textblob import TextBlob
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- TOKEN DEL BOT (usa variable de entorno en Render) ---
TOKEN = os.environ.get("TOKEN")

# --- CONFIGURAR VOZ ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # puedes probar cambiar a voices[1]

# --- MENSAJES BASE SEGÚN SENTIMIENTO ---
mensajes = {
    "positivo": [
        "¡Me alegra escuchar eso! 😄 Sigue así bro, que todo te está saliendo bien.",
        "Eso suena genial 😎, me gusta verte tan motivado.",
        "Wow, qué buena vibra transmites. ¡Esa energía atrae cosas buenas! ✨"
    ],
    "negativo": [
        "Hey bro, tranquilo… a veces toca estar mal, pero eso también te hace más fuerte 💪",
        "Todo pasa por algo, incluso lo que duele. No te rindas, estoy contigo 💬",
        "Respira hondo, bro. Mañana será un nuevo día lleno de oportunidades 🌅"
    ],
    "neutral": [
        "Gracias por contármelo, bro 😊. Me gusta escucharte.",
        "Entiendo cómo te sientes, todo tiene su ritmo.",
        "A veces no se trata de estar bien o mal, solo de seguir adelante 💭"
    ]
}

# --- ANALIZAR SENTIMIENTO DEL TEXTO ---
def analizar_sentimiento(texto):
    polaridad = TextBlob(texto).sentiment.polarity
    if polaridad > 0.1:
        return "positivo"
    elif polaridad < -0.1:
        return "negativo"
    else:
        return "neutral"

# --- DETECTAR EMOCIÓN POR VOZ ---
def detectar_emocion_por_voz():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎙️ Di algo bro, te escucho...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Tú dijiste: {texto}")
        return texto
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

# --- RESPUESTA PRINCIPAL ---
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    estado = analizar_sentimiento(texto)
    respuesta = random.choice(mensajes[estado])

    await update.message.reply_text(respuesta)
    engine.say(respuesta)
    engine.runAndWait()

# --- COMANDO /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bro 😎 soy tu Asistente Emocional 2.0. Puedes escribirme o hablarme.")
    engine.say("Hola bro, soy tu asistente emocional. Cuéntame cómo te sientes.")
    engine.runAndWait()

# --- MODO VOZ LOCAL ---
def modo_voz_local():
    while True:
        texto = detectar_emocion_por_voz()
        if texto:
            estado = analizar_sentimiento(texto)
            respuesta = random.choice(mensajes[estado])
            print(f"Asistente: {respuesta}")
            engine.say(respuesta)
            engine.runAndWait()
        else:
            print("No entendí bro, intenta de nuevo 🎧")

# --- CREAR BOT TELEGRAM ---
def main():
    if TOKEN:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
        print("🤖 Asistente emocional activo en Telegram...")
        app.run_polling()
    else:
        print("⚙️ No se detectó TOKEN, iniciando en modo de voz local 🎤")
        modo_voz_local()

if __name__ == "__main__":
    main()

