from .constants import BASE_CONFIG

def init_config(ibutils, client_api_config):
  """
  initializes snowflake config
  """
  try:
    local_config_path = BASE_CONFIG.FILEPATH
    config = ibutils.read_resource_file(resource_file=BASE_CONFIG.FILENAME,
                                        local_config_path=local_config_path)
    config.update(client_api_config)
    return config, None
  except Exception as errmsg:
    raise Exception(str(errmsg))