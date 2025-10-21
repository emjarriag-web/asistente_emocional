import os
import sounddevice as sd
import numpy as np
import torch
import torchaudio
import asyncio
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pyttsx3
import random

# =====================================================
# CONFIGURACIÓN TELEGRAM
# =====================================================

TOKEN = os.environ.get("TOKEN")  # Tu token se carga como variable de entorno en Render o local

# =====================================================
# CONFIGURACIÓN DE VOZ
# =====================================================

engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('volume', 0.9)

# =====================================================
# MODELO DE DETECCIÓN DE EMOCIONES (IA REAL)
# =====================================================

print("⏳ Cargando modelo de emociones...")
modelo_nombre = "superb/wav2vec2-base-superb-er"
extractor = AutoFeatureExtractor.from_pretrained(modelo_nombre)
modelo = AutoModelForAudioClassification.from_pretrained(modelo_nombre)
labels = modelo.config.id2label
print("✅ Modelo cargado correctamente.")

# =====================================================
# FUNCIÓN: DETECTAR EMOCIÓN POR VOZ
# =====================================================

def detectar_emocion(audio, sr=16000):
    # Reajustar audio a 16kHz
    if sr != 16000:
        audio = torchaudio.functional.resample(torch.tensor(audio), sr, 16000)
        sr = 16000

    inputs = extractor(audio.squeeze().numpy(), sampling_rate=sr, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = modelo(**inputs).logits
    pred = torch.argmax(logits, dim=-1)
    emocion = labels[pred.item()]
    return emocion.lower()

# =====================================================
# COMANDO /voz EN TELEGRAM
# =====================================================

async def escuchar_y_detectar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 Habla durante 5 segundos bro, te estoy escuchando...")

    duration = 5
    grabacion = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32')
    sd.wait()

    audio = grabacion.flatten()
    emocion = detectar_emocion(audio)

    print(f"🧠 Emoción detectada: {emocion.upper()}")

    # Respuestas personalizadas
    respuestas = {
        "happy": [
            "😄 Me alegra escucharte así bro, mantén esa vibra 🔥",
            "💪 Tu voz irradia energía positiva, sigue con todo.",
            "😎 Estás brillando, bro. No pares."
        ],
        "angry": [
            "😡 Tranquilo bro, no dejes que la ira te controle 💪",
            "🧘 Respira... nada vale más que tu paz.",
            "🔥 Convierte ese enojo en motivación para mejorar."
        ],
        "sad": [
            "😢 Te noto bajoneado bro, todo mejora, créeme ❤️",
            "🌈 Los días malos también se acaban. Vas a estar bien.",
            "🫶 No te rindas bro, los mejores días aún no llegan."
        ],
        "fear": [
            "😨 No dejes que el miedo te frene bro, tú puedes con todo.",
            "🦾 El miedo solo es una señal de que estás creciendo.",
            "💭 Recuerda: el valor no es no tener miedo, sino actuar a pesar de él."
        ],
        "neutral": [
            "😐 Te siento tranquilo bro, equilibrio total 😎",
            "☕ Día normal, pero cada momento cuenta.",
            "💭 Todo bien bro, disfruta el presente."
        ]
    }

    # Si no está en el diccionario, que use una neutral
    emocion_key = emocion if emocion in respuestas else "neutral"
    respuesta = random.choice(respuestas[emocion_key])

    # Enviar mensaje en Telegram
    await update.message.reply_text(respuesta)

    # Respuesta hablada
    engine.say(respuesta)
    engine.runAndWait()


# =====================================================
# COMANDO /start
# =====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ¡Hola bro! Soy Asistente Emocional V2. Usa /voz para que te escuche 🎧")


# =====================================================
# MAIN BOT
# =====================================================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("voz", escuchar_y_detectar))

    print("🚀 Asistente Emocional V2 corriendo... 🎤")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
