import imaplib
import email
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Create logger 
logger = logging.getLogger(__name__)
handler = logging.FileHandler('mail_reader.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MailReader:
    def __init__(self):
        self.host = os.environ.get('MAIL_HOST') or 'host'
        self.username = os.environ.get('MAIL_USERNAME') or 'username'
        self.password = os.environ.get('MAIL_PASSWORD') or 'password'
        self.download_folder = './data/downloaded_pdfs/'
        self.processed_folder = './data/processed_pdfs/'
        self.clients = {
            'hermeco': {
                'name': 'C.I. Hermeco S.A.',
                'keywords': ["@offcorss.com"],
            },
            'almacenes exito sa': {
                'name': 'Almacenes éxito s.a.',
                'keywords': ['@grupo-exito.com', "rarodriguezr@grupo-exito.com"],
            },
            'comodin': {
                'name': 'COMODIN S.A.S',
                'keywords': ['comodin s.a.s.', "luisa.morales@gco.com.co"],
            },
            'mercadeo y moda sas': {
                'name': 'MERCADEO Y MODA S.A.S.',
                'keywords': ["chevignon", "MERCADEO Y MODA S.A.S.", "mercadeo y moda s.a.s.", "mercadeo y moda sas", "MERCADEO Y MODA S.A.S"],
            },
        }

    def save_attachment(self, msg, client):
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename and filename.endswith('.pdf') or filename.endswith('.PDF'):
                download_folder = os.path.join(self.download_folder, client)
                processed_folder = os.path.join(self.processed_folder, client)
                download_path = os.path.join(download_folder, filename)
                os.makedirs(os.path.dirname(os.path.join(download_folder, filename)), exist_ok=True)
                os.makedirs(os.path.dirname(os.path.join(processed_folder, filename)), exist_ok=True)
                base, ext = os.path.splitext(download_path)
                new_file_path = base + ext.lower()
                new_file_name = os.path.basename(new_file_path)
                if new_file_name not in os.listdir(processed_folder):
                    with open(new_file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    logger.info(f'Downloaded {download_path}')
                else:
                    logger.info(f'{filename} already exists in processed folder')
                break

    def download_pdfs(self):
        mail = imaplib.IMAP4_SSL(self.host)
        mail.login(self.username, self.password)
        mail.select('inbox')
        typ, message_numbers = mail.search(None, 'ALL')
        for num in message_numbers[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            for part in msg.walk():
                # each part is a either non-multipart, or another multipart message
                # that contains further parts... Message is organized like a tree
                if part.get_content_type() == 'text/plain':
                    mail_body = part.get_payload(decode=True) # prints the raw text
                    str_mail_body = mail_body.decode('utf-8')
                    for client in self.clients:
                        for keyword in self.clients[client]['keywords']:
                            if keyword in str_mail_body.lower():
                                self.save_attachment(msg, client)
                                break
        mail.close()
        mail.logout()
        logger.info('Downloaded all pdfs. Waiting for next run')

if __name__ == '__main__':
    curdir = os.getcwd()
    mail_reader = MailReader()
    mail_reader.download_pdfs()