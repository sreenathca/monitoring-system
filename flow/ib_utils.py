import json
import logging
from instabase.ocr.client.libs.ibocr import ParsedIBOCRBuilder


class IBUtils:
    def __init__(self, clients):
        try:
            self.clients = clients
        except Exception as errmsg:
            return None, str(errmsg)

    def list_directory_content(self, dir_path):
        try:
            directory_content = []
            file_list, err = self.clients.ibfile.list_dir(dir_path, None)
            if err:
                raise Exception(err)
            for node in file_list.nodes:          
                directory_content.append(node.as_dict())
            return directory_content, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def is_dir(self, dir_path):
        try:
            return self.clients.ibfile.is_dir(dir_path), None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def is_file(self, dir_path):
        try:
            return self.clients.ibfile.is_file(dir_path), None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def get_ibmsg_files(self, folder_path):
        try:
            folder_content, err = self.list_directory_content(folder_path)
            if err:
                raise Exception(err)
            ibmsg_nodes = []
            for node in folder_content:
                if node['type'] == 'folder':
                    continue
                if node['name'].split(".")[-1] == 'ibmsg':
                    ibmsg_nodes.append(node)
            return ibmsg_nodes, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def get_ibocr_records(self, file_path):
        try:
            file_content = self.clients.ibfile.open(file_path).read()
            builder, err = ParsedIBOCRBuilder.load_from_str(file_path, file_content)
            if err:
                raise Exception(f"Error in creating builder: {err}")
            ibocr_records = builder.get_ibocr_records()
            return ibocr_records, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def read_ibmsg(self, file_path):
        try:
            ibocr_records = self.get_ibocr_records(file_path)
            json_text = {}
            for ibocr_record in ibocr_records:
                refined_phrases, _ = ibocr_record.get_refined_phrases()
                for phrase in refined_phrases:
                    column_name = phrase.get_column_name()
                    json_text[column_name] = phrase.get_column_value()
            return json_text, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def parse_transaction_table(self, transaction_table):
        try:
            parsed_tt = []
            json_tt = json.loads(transaction_table)
            headers = json_tt[0]
            for row in json_tt[1:]:
                row_dict = {}
                for idx, header in enumerate(headers):
                    row_dict[header] = row[idx]
                parsed_tt.append(row_dict)
            return parsed_tt, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def read_resource_file(self, resource_file, local_config_path):
        try:
            if err:
                raise err
            snowflake_config, err = self.clients.resource_reader.load_file(resource_file)
            if err:
                msg = f'Could not load the resource file {resource_file}'
                logging.info(f'{msg}')
                logging.info(f"Trying to read config from local path...{local_config_path}")
                try:
                    snowflake_config = self.clients.ibfile.open(local_config_path, "rb").read()
                except:
                    snowflake_config = None
                    raise Exception(f"Can't find the config at the following path: {local_config_path}")
            config = json.loads(snowflake_config)
            return config, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def read_ibfile_json(self, filepath):
        try:
            with self.clients.ibfile.open(filepath, "w") as f:
                json_data = json.load(f)
            return json_data, None
        except Exception as errmsg:
            return None, str(errmsg)

    def write_ibfile_json(self, file_content, filepath):
        try:
            with self.clients.ibfile.open(filepath, "w") as f:
                json.dumps(file_content, f)
            return True, None
        except Exception as errmsg:
            return None, str(errmsg)