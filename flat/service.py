from django.core.mail import send_mail

def send_contact(email, author, phone, message):
    send_mail(
        f'Обращение от {author}, {email}, номер - {phone}',
        message=message,
        from_email='noreplyarenda@gmail.com',
        recipient_list=['noreplyarenda@gmail.com',],
        fail_silently=False,
    )