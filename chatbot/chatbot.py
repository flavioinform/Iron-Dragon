import requests
import json
from datetime import datetime
import os

class Chatbot:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "llama3"
        self.info_empresa = {
            "nombre": "Iron Dragon",
            "productos": [
                "Suplementos deportivos",
                "Proteínas",
                "Creatinas",
                "Ropa deportiva",
                "Accesorios fitness",
                "Equipos de entrenamiento",
                "Vitaminas y minerales"
            ],
            "servicios": [
                "Envíos a todo Chile",
                "Asesoría nutricional",
                "Descuentos para socios",
                "Retiro en tienda",
                "Soporte por WhatsApp"
            ],
            "envios": {
                "tiempo": "24-72 horas a todo Chile",
                "costo": "Gratis sobre $40.000, $3.000 bajo ese monto",
                "cobertura": "Todo Chile",
                "tracking": "Seguimiento por correo y WhatsApp"
            },
            "pagos": [
                "Tarjetas de crédito y débito",
                "Transferencias bancarias",
                "Webpay",
                "Mercado Pago"
            ],
            "horarios": {
                "lunes_viernes": "10:00 - 19:00",
                "sabado": "10:00 - 14:00",
                "domingo": "Cerrado",
                "soporte_online": "24/7 por WhatsApp"
            },
            "contacto": {
                "telefono": "+56 9 1234 5678",
                "email": "contacto@irondragon.cl",
                "whatsapp": "+56 9 1234 5678",
                "direccion": "Av. Arturo Prat 123, Iquique"
            },
            "politicas": {
                "devolucion": "15 días para devoluciones",
                "cambio": "7 días para cambios",
                "garantia": "6 meses en productos seleccionados",
                "privacidad": "Datos protegidos según ley chilena"
            }
        }
        self.archivo_historial = "historial_irondragon.json"
        self.cargar_historial()
        
    def cargar_historial(self):
        try:
            if os.path.exists(self.archivo_historial):
                with open(self.archivo_historial, 'r', encoding='utf-8') as f:
                    self.historial = json.load(f)
            else:
                self.historial = []
        except:
            self.historial = []
    
    def guardar_historial(self):
        try:
            with open(self.archivo_historial, 'w', encoding='utf-8') as f:
                json.dump(self.historial[-100:], f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def crear_prompt_sistema(self, mensaje_usuario):
        contexto_previo = ""
        if len(self.historial) > 0:
            contexto_previo = "\n\nConversaciones recientes:\n"
            for conv in self.historial[-5:]:
                contexto_previo += f"Cliente: {conv.get('mensaje', '')}\n"
                contexto_previo += f"Asistente: {conv.get('respuesta', '')}\n"
        
        prompt = f"""Eres un asistente de atención al cliente experto para {self.info_empresa['nombre']}.

INFORMACIÓN DE LA EMPRESA:

🏪 PRODUCTOS DISPONIBLES:
{chr(10).join(f'• {producto}' for producto in self.info_empresa['productos'])}

🚚 ENVÍOS Y ENTREGA:
• Tiempo: {self.info_empresa['envios']['tiempo']}
• Costo: {self.info_empresa['envios']['costo']}
• Cobertura: {self.info_empresa['envios']['cobertura']}
• Tracking: {self.info_empresa['envios']['tracking']}

💳 MÉTODOS DE PAGO:
{chr(10).join(f'• {pago}' for pago in self.info_empresa['pagos'])}

🕐 HORARIOS DE ATENCIÓN:
• Lunes a Viernes: {self.info_empresa['horarios']['lunes_viernes']}
• Sábados: {self.info_empresa['horarios']['sabado']}
• Domingos: {self.info_empresa['horarios']['domingo']}
• Soporte Online: {self.info_empresa['horarios']['soporte_online']}

📞 CONTACTO:
• Teléfono: {self.info_empresa['contacto']['telefono']}
• Email: {self.info_empresa['contacto']['email']}
• WhatsApp: {self.info_empresa['contacto']['whatsapp']}
• Dirección: {self.info_empresa['contacto']['direccion']}

🛡️ SERVICIOS ADICIONALES:
{chr(10).join(f'• {servicio}' for servicio in self.info_empresa['servicios'])}

📋 POLÍTICAS:
• Devolución: {self.info_empresa['politicas']['devolucion']}
• Cambio: {self.info_empresa['politicas']['cambio']}
• Garantía: {self.info_empresa['politicas']['garantia']}
• Privacidad: {self.info_empresa['politicas']['privacidad']}

{contexto_previo}

INSTRUCCIONES:
- Responde de manera amigable, profesional y útil
- Usa emojis apropiados para hacer la conversación más amena
- Máximo 4 oraciones por respuesta
- Si no sabes algo específico, ofrece contactar con un especialista
- Siempre sugiere productos o servicios relevantes cuando sea apropiado

Cliente: {mensaje_usuario}
Asistente:"""
        
        return prompt

    def conectar_ollama(self, mensaje):
        try:
            prompt_sistema = self.crear_prompt_sistema(mensaje)
            data = {
                "model": self.model,
                "prompt": prompt_sistema,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200,
                    "stop": ["Cliente:", "Usuario:", "Asistente:"]
                }
            }
            response = requests.post(self.base_url, json=data, timeout=60)
            if response.status_code == 200:
                resultado = response.json()
                respuesta = resultado['response'].strip()
                if "Asistente:" in respuesta:
                    respuesta = respuesta.split("Asistente:")[-1].strip()
                if "Cliente:" in respuesta:
                    respuesta = respuesta.split("Cliente:")[0].strip()
                return {
                    'respuesta': respuesta,
                    'confianza': 0.9,
                    'tipo_ia': 'ollama_llama3.2',
                    'error': None
                }
            else:
                return {
                    'respuesta': f"Error en Ollama: {response.status_code}",
                    'confianza': 0.1,
                    'tipo_ia': 'ollama_error',
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                'respuesta': f"Error de conexión con Ollama: {str(e)}",
                'confianza': 0.1,
                'tipo_ia': 'ollama_error',
                'error': str(e)
            }

    def procesar_mensaje(self, mensaje_cliente):
        print("🔄 Consultando Ollama (llama3.2)...")
        respuesta_ia = self.conectar_ollama(mensaje_cliente)
        conversacion = {
            'timestamp': datetime.now().isoformat(),
            'mensaje': mensaje_cliente,
            'respuesta': respuesta_ia['respuesta'],
            'confianza': respuesta_ia['confianza'],
            'tipo_respuesta': respuesta_ia['tipo_ia'],
            'error': respuesta_ia['error']
        }
        self.historial.append(conversacion)
        self.guardar_historial()
        return conversacion

    def chatbot_interactivo(self):
        print("\n🤖 CHATBOT IRON DRAGON")
        print("=" * 40)
        print("💬 ¡Hola! Soy tu asistente de Iron Dragon")
        print("🛍️ Puedo ayudarte con productos, envíos, pagos y más")
        print("✨ Escribe 'salir' para terminar")
        print("=" * 40)
        while True:
            mensaje = input("\n👤 Tú: ")
            if mensaje.lower() in ['salir', 'exit', 'quit', 'bye']:
                print("\n👋 ¡Gracias por contactar Iron Dragon!")
                print("🛒 ¡Te esperamos pronto!")
                break
            if mensaje.strip() == "":
                continue
            respuesta = self.procesar_mensaje(mensaje)
            print(f"\n🤖 Asistente: {respuesta['respuesta']}")
            if respuesta['error']:
                print(f"⚠️ Error técnico: {respuesta['error']}")
                print("📞 Puedes contactarnos directamente al +56 9 1234 5678")

def main():
    try:
        chatbot = Chatbot()
        chatbot.chatbot_interactivo()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("🔧 Asegúrate de que Ollama esté ejecutándose en http://localhost:11434")

if __name__ == "__main__":
    main()