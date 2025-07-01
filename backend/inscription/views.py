# backend/inscription/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import InscricaoSerializer

class InscricaoAPIView(generics.CreateAPIView):
    """
    Este é o nosso endpoint principal para receber novas inscrições.
    Ele aceita apenas requisições POST.
    """
    serializer_class = InscricaoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            # Retorna uma resposta de sucesso imediata para o frontend.
            # O trabalho pesado (PDFs, e-mails) está a acontecer em segundo plano.
            return Response(
                {"message": "Inscrição recebida com sucesso! Em breve, o responsável receberá um e-mail de confirmação."},
                status=status.HTTP_202_ACCEPTED
            )
        # A linha abaixo não é estritamente necessária por causa do raise_exception=True,
        # mas é uma boa prática.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
