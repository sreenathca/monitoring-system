import requests
import json
import logging
from .api import API
from .ib_utils import IBUtils


class DB:
    def __init__(self, instabase_url, username, workspace, db_name, auth_token, **kwargs):
        try:
            self.base_url = f'{instabase_url}/api/v1/databases/{username}/{workspace}/databases'
            self.db_url = f'{self.base_url}/{db_name}'
            _, err = self.__setup_api(auth_token)
            if err:
                raise Exception(err)
            self.clients = kwargs.get('clients', None)
        except Exception as errmsg:
            logging.error(f"Error trying to initialize the DB: {errmsg}")
            raise Exception(errmsg)

    def __setup_api(self, auth_token):
        try:
            self.api = API()
            self.api.default_headers = {'Authorization': f'Bearer {auth_token}'}
            return True, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def init_db(self, sql_file_path):
        try:
            init_db_commands, err = self.clients.ibfile.read_file(sql_file_path)
            if err:
                raise Exception(err)
            query_out, err = self.execute_query(init_db_commands)
            if err:
                raise Exception(err)
            return query_out, None
        except Exception as errmsg:
            logging.error(f"Error in init_db: {err}")
            return None, str(errmsg)
    
    def execute_query(self, query):
        try:
            data = json.dumps({"query": query})
            logging.info(f"Executing query: {query}")
            response, err = self.api.post(url=self.db_url, data=data)
            if err:
                raise Exception(err)
            resp_dict = response.json()
            return resp_dict, None
        except Exception as errmsg:
            logging.error(f"Error in execute_query: {errmsg}")
            return None, str(errmsg)
    
    def bulk_insert(self, table_name, values_list):
        try:
            data = json.dumps({'values': values_list})
            url = f"{self.db_url}/{table_name}"
            response, err = self.api.post(url=url, data=data)
            if err:
                raise Exception(err)
            resp_dict = response.json()
            return resp_dict, None
        except Exception as errmsg:
            logging.error(f"Error in bulk_insert: {errmsg}")
            return None, str(errmsg)
