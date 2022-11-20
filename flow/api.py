import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
import logging

class API:
  def __init__(self, **kwargs):
    try:
      self.http = None
      self.default_headers = None
      self.create_session()
      self.set_retry(kwargs)
    except Exception as errmsg:
      raise Exception(f"Error initializing API set: {errmsg}")

  def create_session(self):
    try:
      self.http = requests.Session()
    except Exception as errmsg:
      raise Exception(f"Could not create session as {errmsg}")

  def set_retry(self, num_retries=3,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS"], **kwargs):
    retry_strategy = Retry(
                        total = num_retries,
                        status_forcelist = status_forcelist,
                        method_whitelist = method_whitelist
                    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    self.http.mount("https://", adapter)
    self.http.mount("http://", adapter)

  def __handle_fail_response(self, response=None):
    try:
      if response is None:
        try:
          response = self.response
        except Exception as errmsg:
          raise Exception("response ha not been set")
      err_dict = {
          'error_code': response.status_code,
          'error_msg': response.reason
        }
      return err_dict
    except Exception as errmsg:
      err = f"Could not handle response failure: {errmsg}"
      return str(err)

  def __request(self, method, url, **kwargs):
    try:
      kwargs = self.update_default_header()
      self.response = self.http.request(method=method, url=url, **kwargs)
      if not self.response.ok:
        err = self.__handle_fail_response()
        raise Exception(err)
      return self.response, None
    except Exception as errmsg:
      return None, str(errmsg)

  def get_session(self):
    try:
      if not self.http:
        err = "session not created"
        raise Exception(err)
      return self.http, None
    except Exception as errmsg:
      return None, str(errmsg)

  def get(self, url, **kwargs):
    try:
      self.response, err = self.__request('get', url, **kwargs)
      if err:
        raise Exception(err)
      return self.response, None
    except Exception as errmsg:
      return None, str(errmsg)

  def patch(self, url, **kwargs):
    try:
      self.response, err = self.__request('patch', url, **kwargs)
      if err:
        raise Exception(err)
      return self.response, None
    except Exception as errmsg:
      return None, str(errmsg)

  def post(self, url, **kwargs):
    try:
      self.response, err = self.__request('post', url, **kwargs)
      if err:
        raise Exception(err)
      return self.response, None
    except Exception as errmsg:
      return None, str(errmsg)

  def delete(self, url, **kwargs):
    try:
      self.response, err = self.__request('delete', url, **kwargs)
      if err:
        raise Exception(err)
      return self.response, None
    except Exception as errmsg:
      return None, str(errmsg)

  def get_json(self, response=None):
    try:
      if response is None:
        try:
          response = self.response
        except Exception as errmsg:
          raise Exception("response has not been set")
      return response.json(), None
    except Exception as errmsg:
      return None, str(errmsg)

  def get_headers(self, keyword=None):
    try:
      if response is None:
        try:
          response = self.response
        except Exception as errmsg:
          raise Exception("response has not been set")
      headers = dict(response.headers)
      if keyword is not None:
        return headers.get(keyword), None
      return headers, None
    except Exception as errmsg:
      return None, str(errmsg)

  @property
  def default_headers(self):
    return self.default_headers

  @default_headers.setter
  def default_headers(self, headers):
    self.default_headers = headers


  def update_default_header(self, kwargs):
    try:
      if 'headers' not in kwargs.keys() and self.default_headers is not None:
        kwargs['headers'] = self.default_headers
      elif self.default_headers is not None:
        kwargs['headers'].update(self.default_headers)
      return kwargs
    except Exception as errmsg:
      return None, str(errmsg)