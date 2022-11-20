import json
import requests
from requests.exceptions import HTTPError
import logging

# Importing custom packages
from .api import API

class Monitor():
    __endpoints = {
        'list_jobs': '/jobs/list',
        'flow_results': '/flow_binary/results',
        'job_metrics': '/flow_metrics/jobs',
        'job_status': '/jobs/status'
    }

    def __init__(self, config, **kwargs):
        try:
            instabase_url = config.get('INSTABASE_URL', 'https://www.instabase.com')
            auth_token = config.get('AUTH_TOKEN')
            self.base_url = f'{instabase_url}/api/v1'
            self.accepted_flows = config.get('MONITORED_FLOWS')
            logging.info(f"Running Monitor job for {self.accepted_flows}")
            _, err = self.__setup_api(auth_token)
            if err:
                logging.error(f"Could not set up API: {err}")
                raise Exception(f"Error setting up API: {err}")
        except Exception as errmsg:
            raise Exception(errmsg)
    
    def __setup_api(self, auth_token):
        try:
            self.api = API()
            self.api.default_headers = {'Authorization': f'Bearer {auth_token}'}
            return True, None
        except Exception as errmsg:
            return None, str(errmsg)
    
    def __get_url(self, endpoint):
        endpoint_url = self.__endpoints.get(endpoint, 'None')
        return self.base_url + endpoint_url

    def __get_call(self, url, **kwargs):
        headers = kwargs.get('headers', {})
        headers.update({'Authorization': f'Bearer {self.auth_token}'})
        if 'headers' in kwargs.keys():
            del kwargs['headers']
        response = self.https.get(url, headers=headers, **kwargs)
        if not response.ok:
            return None, response.reason
        return response.json(), None
    
    def __job_timefilter(self, finish_time, job):
        if job['finish_timestamp'] < finish_time:
            return False
        return True
    
    def __accepted_flow_filter(self, job):
        if any([True for flow in self.accepted_flows if f'{flow}.ibflow' in job['flow_path']]):
            return True
        return False

    def __list_jobs(self, finish_time, limit=200, next_page_url=None):
        try:
            __endpoint = 'list_jobs'
            jobs = []
            if next_page_url:
                response, err = self.api.get(url=next_page_url)
            else:
                url = self.__get_url(__endpoint)
                arguments = locals()
                params = {'sort_by': 'finish_time'}
                for k, v in arguments.items():
                    if k == 'next_page_url':
                        continue
                    params[k] = v
                response, err = self.api.get(url=url, params=params)
            if err:
                raise Exception(err)
            resp_dict = response.json()
            for job in resp_dict['jobs']:
                if not self.__job_timefilter(finish_time, job):
                    break
                if not self.__accepted_flow_filter(job):
                    continue
                jobs.append(job)
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

    def __get_flow_results(self, ibresults_path):
        try:
            __endpoint = 'flow_results'
            url = self.__get_url(__endpoint)
            args = {
                'ibresults_path': ibresults_path,
                'options': {'include_checkpoint_results': True},
                'file_offset': 0
            }
            json_data = json.dumps(args)
            resp_dict, err = self.__get_call(url=url, data=json_data)
        except Exception as errmsg:
            return None, str(errmsg)