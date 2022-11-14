import json
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import HTTPError
import logging

class Monitor:
    __endpoints = {
        'list_jobs': '/jobs/list'
    }

    def __init__(self, **kwargs):
        try:
            config = self.__read_config()
            instabase_url = config.get('INSTABASE_URL', 'https://www.instabase.com')
            self.auth_token = config.get('AUTH_TOKEN')
            self.base_url = f'{instabase_url}/api/v1'
            _, err = self.__setup_api()
            if err:
                raise Exception(f"Error setting up API: {err}")
        except Exception as errmsg:
            raise Exception(errmsg)
    
    def __setup_api(self):
        try:
            self.https = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[ 500, 502, 503, 504 ])
            self.https.mount('https://', HTTPAdapter(max_retries=retries))
            return True, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def __read_config(self):
        pass
    
    def __get_url(self, endpoint):
        endpoint_url = self.__endpoints.get(endpoint, 'None')
        return self.base_url + endpoint_url

    def __get_call(self, url, **kwargs):
        params = kwargs.get('params', None)
        headers = kwargs.get('headers', {})
        headers.update({'Authorization': f'Bearer {self.auth_token}'})
        response = self.https.get(url, params=params)
        if not response.ok:
            return None, response.reason
        return response.json(), None

    def __list_jobs(self, limit=200, offset=None, from_timestamp=None, to_timestamp=None,
                    state=None, user=None, tags=None, pipeline_ids=None, review_state=None,
                    job_id=None, job_ids=None, reviewer=None, next_page_url=None):
        try:
            __endpoint = 'list_jobs'
            jobs = []
            if next_page_url:
                resp_dict, err = self.__get_call(url=next_page_url)
            else:
                url = self.__get_url(__endpoint)
                arguments = locals()
                params = {}
                for k, v in arguments.items():
                    if k == 'next_page_url':
                        continue
                    params[k] = v
                resp_dict, err = self.__get_call(url=url, params=params)
            if err:
                raise Exception(err)
            jobs.extend(resp_dict['jobs'])
            if len(jobs) == 0:
                return [], None
            read_more = False
            if limit is None:
                read_more = True
            elif limit > len(jobs):
                read_more = True
            if resp_dict['next_page'] and read_more:
                temp_jobs, err = self.__list_jobs(next_page_url=resp_dict['next_page'])
                if err:
                    raise Exception(err)
                jobs.extend(temp_jobs)
            return jobs, None
        except Exception as errmsg:
            return None, str(errmsg)