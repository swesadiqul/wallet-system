from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from wallet.serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('Hello World')

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        user = request.user

        if id and str(id) != str(user.id):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'You can only view your own wallet.'}, status=status.HTTP_400_BAD_REQUEST)
        
        wallet = request.user.wallet
        transactions = wallet.transactions.order_by('-created_at')

        wallet_serializer = WalletSerializer(wallet).data
        transactions_serializer = TransactionSerializer(transactions, many=True).data
        return Response({'status': 'success', 'code': status.HTTP_200_OK, 'balance': wallet_serializer['balance'], 'transactions': transactions_serializer})

    def post(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        user = request.user
        amount = request.data.get('amount')

        if id and str(id) != str(user.id):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'You can only debit your own wallet.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            wallet = request.user.wallet
            wallet.add_money(amount)
            return Response({'status': 'success', 'code': status.HTTP_201_CREATED, 'message': 'Funds successfully added!', 'balance': wallet.get_balance()}, status=status.HTTP_201_CREATED)
        except (ValueError, TypeError):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        amount = request.data.get('amount')
        user = request.user

        if id and str(id) != str(user.id):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'You can only credit your own wallet.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            wallet = request.user.wallet
            wallet.spend_money(amount)
            return Response({'status': 'success', 'code': status.HTTP_201_CREATED, 'message': 'Funds successfully spent!', 'balance': wallet.get_balance()}, status=status.HTTP_201_CREATED)
        except (ValueError, TypeError):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
