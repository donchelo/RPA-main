from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from json_parser.main import JsonParser
import logging

load_dotenv()
json_parser = JsonParser()

# Create logger 
logger = logging.getLogger(__name__)
handler = logging.FileHandler('assistant.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise Exception("OPENAI_API_KEY not found")

client = OpenAI(api_key=openai_api_key)

class Assistant:
    def __init__(self):
        self.file = None
        self.assistant = None
        self.message_body = """responde en un formato JSON estructurado."""
        self.assistant_id = None
        self.messages = None
        self.assistants = None

    def create_assistant(self, file=None):
        self.assistant = client.beta.assistants.create(
            name = "Tamaprint Assistant - Order Reader",
            instructions = """
Como Order Loader Hermeco, tu función principal es leer y analizar órdenes de compra específicamente de 'C.I Hermeco S.A.' y devolver la información en un formato JSON estructurado.
{
"comprador": {
    "nit": // CN890924167
},
"orden_compra": // string
"fecha_entrega": // string
"items": [
    {
        "descripcion": // string
        "codigo": // string
        "cantidad": // number
        "precio_unitario": // (dividir precio unitario sobre 100) number 
        "precio_total": // number
        "fecha_entrega": // string
    }
],
}
Las fechas deben ser en formato DD/MM/AAAA.
""",
            tools = [{"type": "retrieval"}],
            model="gpt-4-1106-preview",
            file_ids = [file.id] if file else [],
        )
        return self.assistant

    def upload_file(self, path):
        file = client.files.create(
            file = open(path, "rb"),
            purpose = "assistants"
        )
        logger.info(f"Uploaded file {file.filename}")
        return file

    def generate_response(self, message_body, file):
        thread = client.beta.threads.create()
        thread_id = thread.id
        message = client.beta.threads.messages.create(
            thread_id = thread_id,
            content = message_body,
            role = "user",
            attachments = [{"tools": [
                {"type":"code_interpreter"},
                {"type":"file_search"}
            ], "file_id": file.id}]
        )
        return message

    def save_txt_file(self, file, message, assistant_id):
        response_messages = self.run_assistant(assistant_id, message.thread_id)
        response_content = "\n".join([response_message.content[0].text.value for response_message in response_messages])
        is_parsable = json_parser.is_parsable(response_content)
        if not is_parsable:
            logger.warning(f"File {file.filename} is not parsable")
            return
        response_content = json_parser.get_json_from_string(response_content)
        
        os.makedirs(os.path.dirname(os.path.join("./data/outputs_txt",f"{file.filename.split('.')[0]}.txt")), exist_ok=True)
        with open(f"./data/outputs_txt/{file.filename.split('.')[0]}.txt", "w") as f:
            f.write(response_content)
            f.close()
            logger.info(f"Saved {file.filename} as .txt")
        self.move_pdf_to_processed(file.filename)
        self.delete_file(file)

    def run_assistant(self, assistant_id, thread_id):
        assistant = client.beta.assistants.retrieve(assistant_id)
        thread = client.beta.threads.retrieve(thread_id=thread_id)
        run = client.beta.threads.runs.create(
            assistant_id = assistant.id,
            thread_id = thread.id,
        )
        while run.status != "completed":
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(thread_id = thread.id, run_id = run.id)
        messages = client.beta.threads.messages.list(thread_id = thread.id)
        logger.info(f"Assistant {assistant.name} finished")
        return messages.data

    def delete_file(self, file):
        client.files.delete(file.id)
        logger.info(f"Deleted file {file.filename}")

    def loop_clients_and_call_assistant(self):
        self.get_all_assistants()
        clients = os.listdir("./data/downloaded_pdfs")
        for client in clients:
            processed_files = os.listdir(f"./data/processed_pdfs/{client}")
            assistant = self.get_assistant_by_name(client)
            if assistant:
                files = os.listdir(f"./data/downloaded_pdfs/{client}")
                for file in files:
                    if file not in processed_files:
                        self.call_assistant(assistant=assistant , file=f"./data/downloaded_pdfs/{client}/{file}")
            else:
                logger.info(f"Client {client} not found in assistants")

    def get_all_assistants(self):
        self.assistants = client.beta.assistants.list().data
        return self.assistants

    def call_assistant(self, assistant, file):
        logger.info(f"Calling assistant {assistant.name} for file {file}")
        file = self.upload_file(file)
        response = self.generate_response(self.message_body, file)
        self.save_txt_file(file, response, assistant.id)
        return response

    def get_assistant_by_name(self, client_name):
        for assistant in [assistant for assistant in self.assistants if assistant.name]:
            name = assistant.name.lower()
            if client_name in name:
                self.assistant = assistant
                return assistant
        logger.info(f"Assistant for client {client_name} not found")
        return None
    
    def move_pdf_to_processed(self, file):
        # search for file in downloaded_pdfs
        clients = os.listdir("./data/downloaded_pdfs")
        for client in clients:
            files = os.listdir(f"./data/downloaded_pdfs/{client}")
            for file_ in files:
                if file == file_:
                    os.makedirs(os.path.dirname(os.path.join("./data/processed_pdfs", f"{client}/{file}")), exist_ok=True)
                    os.rename( f"./data/downloaded_pdfs/{client}/{file}", f"./data/processed_pdfs/{client}/{file}")
                    logger.info(f"Moved {file} to processed folder")
                    return

if __name__ == '__main__':
    assistant = Assistant()
    assistant.loop_clients_and_call_assistant()
