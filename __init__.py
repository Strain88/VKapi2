__version__ = '0.9.5'

from VKapi2.exceptions import ApiException
from VKapi2.api import Api
from VKapi2.api import ApiHelper

import sys
import logging
import requests

logger = logging.getLogger('VK_api_2')

formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)
#logging in console:
#console_output_handler = logging.StreamHandler(sys.stderr)
#console_output_handler.setFormatter(formatter)
#logger.addHandler(console_output_handler)

#logging to fille:
file_output_handler = logging.FileHandler(filename='VK_api2.log', mode='wb')
file_output_handler.setFormatter(formatter)
logger.addHandler(file_output_handler)

logger.setLevel(logging.ERROR)


class Session(object):
  """
  This class will take stand-alone token and generate requests to VK
  """
  API_URL = "https://api.vk.com/method/{0}"
  CONNECT_TIMEOUT = 5
  READ_TIMEOUT = 9999
  
  
  def __init__(self, access_token):
    self.at = access_token
    """
    Gets stand-alone app token.
    :param access_token: standalone app token.
    """
    
    
  @staticmethod
  def _make_request(method_name, method='get', params=None, files=None, base_url=API_URL, timeout=100):
    """
    Makes a request to VK api.
    :param method_name: Name of the API method to be called. (E.g. 'getUploadServer')
    :param method: HTTP method to be used. GET by default.
    :param params: Optional parameters. Should be a dictionary with key-value pairs.
    :param files: Optional files.
    :return: The result parsed to a JSON dictionary.
     """
    request_url = base_url.format(method_name)
    logger.debug("Request: method={0}, url={1}, params={2}, files={3}".format(method, request_url, params, files))
    read_timeout=Session.READ_TIMEOUT
    if params:
      if 'timeout' in params: read_timeout=params['timeout'] + 10
      r = requests.request(method, request_url, params=params, files=files, timeout=(Session.CONNECT_TIMEOUT, read_timeout))
      logger.debug("This server returned: '{0}'".format(r.text.encode('utf8')))
      return Session._check_result(method_name, r)
    
    
  @staticmethod
  def _check_result(method_name, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
    - The server returned an HTTP response code other than 200
    - The content of the result is invalid JSON.
    - The method call was unsuccessful (The JSON 'ok' field equals False)
    :raises ApiException: if one of the above listed cases is applicable
    :param method_name: The name of the method called
    :param result: The returned result of the method request
    :return: The result parsed to a JSON dictionary.
    """
    if result.status_code != 200:
      msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text.encode('utf8'))
      raise ApiException(msg, method_name, result)
    try:
      result_json = result.json()
    except:
      msg = 'The server returned an invalid JSON response. Response body:\n[{0}]' \
            .format(result.text.encode('utf8'))
      raise ApiException(msg, method_name, result)
    return result_json
