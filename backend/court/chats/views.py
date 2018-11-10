from flask import jsonify, request, g
from flask.views import MethodView

from court.chats.thread_service import ThreadService
from court.users.auth_service import AuthService
from court.errors import AuthorizationError


class MessageAPI(MethodView):
  """
  Provides the view layer API for messages
  """
  def __init__(self, thread_service, auth_service):
    """
    Creates a new MessageAPI object.  Should be called with 
    MessageAPI.as_view(url, thread_service, auth_service) to initialize.

    :param thread_service: a ThreadService instance
    :param auth_service: an AuthService instance
    """
    self.thread_service = thread_service
    self.auth_service = auth_service

  def get(self, thread_id):
    """
    Processes a HTTP GET request for the message REST API.

    :param thread_id: the id of the thread requested
    :return: a Flask HTTP response with a list of thread messages
    """
    auth_service = self.auth_service
    user_id = auth_service.get_current_user_id()

    first = 50
    after_id = -1
    before_id = -1

    if 'first' in request.args:
      first = request.args.get('first')
    if 'after_id' in request.args:
      after_id = request.get('after_id')
    elif 'before_id' in request.args:
      before_id = request.get('before_id')

    messages = self.thread_service.get_messages(user_id, thread_id, first, after_id, before_id)

    return jsonify(messages=messages)
  
class ThreadAPI(MethodView):
  """
  Provides the view layer API for threads
  """
  def __init__(self, auth_service):
    """
    Creates a new ThreadAPI object.  Should be called with 
    ThreadAPI.as_view(url, auth_service) to initialize.

    :param auth_service: an AuthService instance
    """
    self.auth_service = auth_service

  def get(self):
    """
    Processes a HTTP GET request for the thread REST API.

    :return: a Flask HTTP response of all users threads
    """
    user = self.auth_service.get_current_user()

    return jsonify(threads=user.threads)
    