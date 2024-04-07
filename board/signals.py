from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.dispatch import receiver

from board.models import Reply
from sitecore import settings


def send_email(reply, title, template, subscribers_email):
    html_mail = render_to_string(
        template,
        {
            'text': reply,
        }
    )

    message = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()


@receiver(post_save, sender=Reply)
def new_reply(sender, instance, **kwargs):
    if kwargs['created']:
        send_email(instance.content, f'Новый отклик на ваше обьявление({instance.post.title})',
                   'reply_sendmail_author.html', [instance.post.post_author.email])

