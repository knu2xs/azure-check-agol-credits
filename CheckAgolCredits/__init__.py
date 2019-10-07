import base64
import json
import logging
import os
import urllib.request as urllib

from arcgis.gis import GIS
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

# path to where prepped internal AGOL Subscription request document is stored
local_dir = os.path.dirname(os.path.abspath(__file__))
request_form = os.path.join(os.path.dirname(local_dir), 'resources', 'subscription_request.docx')

# variables loaded from environment settings - credentials, access keys, and email addresses
agol_username = os.environ.get('AGOL_USERNAME')
agol_password = os.environ.get('AGOL_PASSWORD')
sendgrid_key = os.environ.get('SENDGRID_KEY')
from_email = f"{os.environ.get('EMAIL_TO')}<{os.environ.get('EMAIL_NAME_TO')}>"
to_email = f"{os.environ.get('EMAIL_TO')}<{os.environ.get('EMAIL_NAME_TO')}>"
admin_email = os.environ.get('EMAIL_ADMIN')
admin_name = os.environ.get('EMAIL_ADMIN_NAME')


def main(mytimer: func.TimerRequest) -> None:

    # create a connection to the ArcGIS instance
    gis = GIS(username=agol_username, password=agol_password)
    logging.info(f'Connected to {gis.properties.name}')

    # if the available credits are less than 500
    if gis.properties.availableCredits < 500:

        logging.info(f'The ArcGIS Online organization, {gis.properties.name}, currently only has ' \
            f'{gis.properties.availableCredits:,} and needs to be rehydrated.')
        
        email_subject = f'Rehydrate Credits for {gis.properties.name} ArcGIS Online Organization'
        email_body = f'<p>The ArcGIS Online organization, {gis.properties.name}, currently only has ' \
            f'{gis.properties.availableCredits :,} credits. Please update the attached form and send it ' \
            f'to <a href="mailto:{admin_email}?subject=Rehydrate%20ArcGIS%20Online%20Organization">' \
            f'{admin_name}</a> to request more.</p>'

        # create the mail object with the recepients
        mail = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=email_subject,
            html_content=email_body
        )

        # read and encode the attachment into base64 in memory
        with open(request_form, 'rb') as attachment_file:
            data = attachment_file.read()
            attachment_file.close()
            encoded_file = base64.b64encode(data).decode()

        # create and attachment object and add it to the mail object
        attachment = Attachment(
            file_content=FileContent(encoded_file),
            file_name=os.path.basename(request_form),
            file_type=FileType('application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
            disposition=Disposition('attachment')
        )
        mail.attachment = attachment

        # try to send the email, and log results
        try:
            sendgrid_client = SendGridAPIClient(sendgrid_key)
            response = sendgrid_client.send(mail)
            logging.info(response.status_code)
            logging.info(response.body)
            logging.info(response.headers)
        except Exception as e:
            logging.exception(e.mail)

    else:
        logging.info(f'The ArcGIS Online organization, {gis.properties.name}, currently has ' \
            f'plenty of credits, {gis.properties.availableCredits:,}.')
