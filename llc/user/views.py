from django.shortcuts import render
from .models import Package
import random
def main(request):
    return render(request, 'user/index.html')

def send(request):


    sender = request.GET.get('sender')
    recipient = request.GET.get('recipient')
    sender_adres = request.GET.get('sender_adres')
    recipient_adres = request.GET.get('recipient_adres')

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    tracking_number = ''
    for i in range(30):
        tracking_number += random.choice(chars)
    package = Package(tracking_number=tracking_number, sender=sender,sender_adres=sender_adres,recipient_adres=recipient_adres, recipient=recipient)
    package.save()
    context = {
        'sender':sender,
        'recipient':recipient,
        'sender_adres':sender_adres,
        'recipient_adres':recipient_adres,
        "tracking_number":tracking_number,

    }
    return render(request, 'user/send.html', context)



def track(request):
    tracking_number = request.GET.get('tracking_number')
    try:
        package = Package.objects.get(tracking_number=tracking_number)
        context = {
            'tracking_number': tracking_number,
            'when': package.when,
            'recipient':package.recipient,
            'sender_adres':package.sender_adres,
            'recipient_adres':package.recipient_adres,
            'sender':package.sender,
        }
    except Package.DoesNotExist:
        context = {
            'tracking_number': tracking_number,
            'error': 'Посылка с таким номером не найдена.',
        }
    return render(request, 'user/track.html', context)