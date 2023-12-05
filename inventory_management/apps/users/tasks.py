from inventory_management.celery.celery import app
from .emails import set_password_link_mail, credential_mail

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(name='set_password_link_mail_task')
def set_password_link_mail_task(activation_link, to_email, user_id):
    logger.info('send set password link mail logger print')
    return set_password_link_mail(activation_link, to_email, user_id)


@app.task(name='credential_mail_task')
def credential_mail_task(activation_link, email, password):
    logger.info('send credential mail logger print')
    return credential_mail(activation_link, email, password)
