import google.generativeai as genai
import json
import time

# 1. CONFIGURACIÓN (Usando la key proporcionada)
API_KEY = "<GOOGLE_API_KEY-PURGADA-DEL-HISTORIAL>"
genai.configure(api_key=API_KEY)

# 2. CONFIGURACIÓN DEL MODELO
model = genai.GenerativeModel(
    model_name='gemini-3.5-flash',
    generation_config={"response_mime_type": "application/json"}
)

# 3. PROMPT OPTIMIZADO
prompt = """
Extrae la información del siguiente texto en formato JSON.
Campos requeridos: nombre_cliente, fecha, numero_orden, monto_total, empresa.

Ejemplo:
Entrada: "Compra de Ana el 1 de mayo, orden 123, total 50 USD en Tienda X"
Salida: {"nombre_cliente": "Ana", "fecha": "1 de mayo", "numero_orden": "123", "monto_total": "50 USD", "empresa": "Tienda X"}

Texto a procesar:
"""

texto_sucio = "Hola, soy Carlos. Te mando el comprobante de la compra del día 15 de junio. El número de orden es ORD-99283 y el total fue de 150.50 USD, aunque pagué 10 USD de envío aparte. La empresa es TechNova Soluciones. Saludos."

# 4. EJECUCIÓN Y MEDICIÓN
print("🚀 Iniciando extracción con Gemini 1.5 Flash...")
start_time = time.time()

try:
    response = model.generate_content(prompt + texto_sucio)
    end_time = time.time()

    data = json.loads(response.text)

    print("\n✅ RESULTADO DE LA EXTRACCIÓN:")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print(f"\n⏱️ Tiempo de respuesta: {end_time - start_time:.2f} segundos")

except Exception as e:
    print(f"❌ Error: {e}")
