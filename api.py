#!-*-coding:utf8-*-
from urllib import urlopen

class Api(object):
  
  def __init__(self, session, **default_api_kwargs):
    self._session=session
    self._defauld_api_kwargs=default_api_kwargs
    self._defauld_api_kwargs.update({'access_token': self._session.at})
    self.stats.trackVisitor()
    
    
  def make_request(self, **request_obj):
    if 'fromApiHelper' in request_obj:
      req = request_obj['fromApiHelper']

      method_url=req.get_method_name()
      method_args=req.get_method_args()
      
      if method_url=="audio.save": #TODO: make this method more practical
        """
        :param link_to_file: required parameter
        """
        self._defauld_api_kwargs.update(method_args)
        upload_vk_url = self.audio.getUploadServer()['response']['upload_url']
        f = method_args.get('link_to_file', "Link is absent")
        opened_audio = urlopen(f)
        audio_file = {'file':('mymusic.mp3', opened_audio)}


        payload={'v': self._defauld_api_kwargs.get('v', '3.0')}
        data = self._session._make_request(r'', method='post', params=payload, files=audio_file, base_url=upload_vk_url)
        
        payload={'audio': data['audio'], 'hash': data['hash'], 'artist': self._defauld_api_kwargs.get('artist', None), 'title': self._defauld_api_kwargs.get('title', None), 'server': int(data['server']),'v': self._defauld_api_kwargs.get('v', '3.0'), 'access_token': self._defauld_api_kwargs.get('access_token', None)}
              
        self._session._make_request(method_url, params=payload)

      self._defauld_api_kwargs.update(req.get_method_args())
      self._defauld_api_kwargs.update({'access_token': self._session.at})
    else:
      msg = '__call__ method in ApiHelper worked wrong. Response body:\n[{0}]' \
            .format(result.text.encode('utf8'))
      raise ApiException(msg, None, None)
    return self._session._make_request(method_url, params=self._defauld_api_kwargs)
    
  
  def __getattr__(self, method_name):
    return ApiHelper(self, method_name)
    
    
class ApiHelper(object):
  
  def __init__(self, api, method_name):
    self._api=api 
    self._method_name=method_name
    self._method_args=None
    
  
  def get_api(self):
    return self._api 
    
    
  def get_method_name(self):
    return self._method_name
    
    
  def get_method_args(self):
    return self._method_args
    
    
  def __repr__(self):
    return "{}(method='{}', args={})".format(
            self.__class__.__name__, self.get_method_name(),
            self.get_method_args())
    
    
  def __getattr__(self, method):
    """
    This is done for audio.save only
    """
    return ApiHelper(self._api, ".".join([self._method_name, method]))
      
      
  def __call__(self, **method_args):
    self._method_args=method_args
    return self._api.make_request(fromApiHelper=self)
