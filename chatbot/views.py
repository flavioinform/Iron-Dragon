from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .chatbot import Chatbot  # Importa la clase Chatbot desde el archivo chatbot.py

class ChatbotView(APIView):
    def post(self, request):
        mensaje = request.data.get('mensaje', '')
        if not mensaje:
            return Response({'error': 'Mensaje vacío'}, status=status.HTTP_400_BAD_REQUEST)
        chatbot = Chatbot()  # Instancia la clase Chatbot
        respuesta = chatbot.procesar_mensaje(mensaje)
        return Response({'respuesta': respuesta['respuesta']})