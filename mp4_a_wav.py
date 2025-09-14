import speech_recognition as sr
import subprocess
import os
import sys

# USA ESTA RUTA EXACTA - LA QUE TIENES INSTALADA
RUTA_FFMPEG = r"C:\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

def verificar_ffmpeg():
    """Verifica si FFmpeg existe en la ruta especificada"""
    if os.path.exists(RUTA_FFMPEG):
        print(f"✅ FFmpeg encontrado en: {RUTA_FFMPEG}")
        return True
    else:
        print(f"❌ FFmpeg NO encontrado en: {RUTA_FFMPEG}")
        return False

def convertir_mp4_a_wav(input_file, output_file):
    """Convierte MP4 a WAV usando la ruta directa a FFmpeg"""
    try:
        comando = [
            RUTA_FFMPEG,
            '-i', input_file,      # Archivo de entrada
            '-vn',                 # Remover video
            '-acodec', 'pcm_s16le', # Códec de audio
            '-ar', '44100',        # Tasa de muestreo
            '-ac', '1',            # Mono (mejor para transcripción)
            '-y',                  # Sobrescribir si existe
            output_file            # Archivo de salida
        ]
        
        print("Ejecutando conversión...")
        result = subprocess.run(comando, capture_output=True, text=True, check=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en conversión: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def transcribir_audio(audio_file):
    """Transcribe audio a texto"""
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            print("Ajustando para ruido ambiental...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Grabando audio...")
            audio = r.record(source)
        
        print("Transcribiendo con Google Speech Recognition...")
        text = r.recognize_google(audio, language="es-ES")
        return text
        
    except sr.UnknownValueError:
        return "❌ No se pudo entender el audio."
    except sr.RequestError as e:
        return f"❌ Error de conexión: {e}"
    except Exception as e:
        return f"❌ Error: {e}"

# --- PROGRAMA PRINCIPAL ---
print("🎵 CONVERSOR DE AUDIO MP4 A TEXTO")
print("=" * 50)

# Verificar FFmpeg
if not verificar_ffmpeg():
    sys.exit(1)

# Archivos
archivo_entrada = "audio.mp4"
archivo_salida = "audio.wav"

# Verificar si existe el archivo de entrada
if not os.path.exists(archivo_entrada):
    print(f"❌ Archivo '{archivo_entrada}' no encontrado!")
    sys.exit(1)

# Convertir MP4 a WAV
print(f"\n🔄 Convirtiendo '{archivo_entrada}' a WAV...")
if convertir_mp4_a_wav(archivo_entrada, archivo_salida):
    print("✅ Conversión exitosa!")
    
    # Transcribir audio
    print("\n🎤 Transcribiendo audio...")
    texto = transcribir_audio(archivo_salida)
    
    # Mostrar resultado
    print(f"\n{'=' * 60}")
    print("📝 TEXTO EXTRAÍDO:")
    print('=' * 60)
    print(texto)
    print('=' * 60)
    
    # Guardar en archivo
    with open("transcripcion.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    
    print("\n💾 Transcripción guardada en 'transcripcion.txt'")
    
else:
    print("❌ Error en la conversión")