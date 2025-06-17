import os
import logging
import json

# Create logger 
logger = logging.getLogger(__name__)
handler = logging.FileHandler('json_parser.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class JsonParser:
    def __init__(self):
        pass

    def get_json_start_end_index(self, string):
        start = string.find('{')
        end = string.rfind('}')
        return start, end

    def get_json_from_string(self, string):
        start, end = self.get_json_start_end_index(string)
        return string[start:end+1]

    def get_json_from_file(self, file):
        with open(file, 'r') as f:
            string = f.read()
            if not self.is_parsable(string):
                logger.warning(f"File {file} is not parsable")
                return None
        return self.get_json_from_string(string)

    def get_json_from_txt_and_save_as_json_file(self, file):
        if json_string := self.get_json_from_file(file):
            json_filename = file.split('/')[-1].split('.')[0] + '.json'
            os.makedirs(os.path.dirname(os.path.join("./data/outputs_json",f"{json_filename}")), exist_ok=True)
            with open(f"./data/outputs_json/{json_filename}", "w") as f:
                json_dict = json.loads(json_string)
                json.dump(json_dict, f, indent=4)
            self.move_txt_to_processed(file)
            return json_string
        else:
            logger.info(f"File {file} is not parsable")

    def loop_txt_directory_and_create_json_files(self):
        os.makedirs("./data/outputs_txt", exist_ok=True)
        directory = "./data/outputs_txt"
        files = os.listdir(directory)
        for file in files:
            if file.endswith(".txt"):
                self.get_json_from_txt_and_save_as_json_file(f"{directory}/{file}")
        logger.info('Parsed all .txt to .json')

    def call_json_parser(self):
        self.loop_txt_directory_and_create_json_files()
        logger.info('Parse json files completed. Waiting for next run')

    def is_parsable(self, string):
        return '{' in string and '}' in string

    def move_txt_to_processed(self, file):
        os.makedirs(os.path.dirname(os.path.join("./data/processed_txt")), exist_ok=True)
        clients = os.listdir("./data/processed_pdfs")
        for client in clients:
            files = os.listdir(f"./data/processed_pdfs/{client}")
            for file_ in files:
                filename = file_.split('.')[0]
                if filename in file:
                    destination = f"./data/processed_txt/{client}/{filename}.txt"
                    os.makedirs(os.path.dirname(destination), exist_ok=True)
                    if not os.path.exists(destination):
                        os.rename(file, destination)
                        logger.info(f"Moved {file} to processed_txt")
                    else:
                        logger.info(f"File {destination} already exists. Skipping move.")
                    return

    def move_json_to_processed(self, file):
        clients = os.listdir("./data/processed_txt")
        for client in clients:
            files = os.listdir(f"./data/processed_txt/{client}")
            for file_ in files:
                filename = file_.split('.')[0]
                if filename in file:
                    os.makedirs(os.path.dirname(os.path.join("./data/processed_json", f"{client}/{filename}.json")), exist_ok=True)
                    os.rename(f"./data/outputs_json/{file}", f"./data/processed_json/{client}/{filename}.json")
                    logger.info(f"Moved {file} to processed_json")
                    return
        logger.info(f"File {file} not found in processed_txt/{client}. filename: {filename}")
        return

if __name__ == '__main__':
    json_parser = JsonParser()
    json_parser.call_json_parser()