from models.user import UserModel
from werkzeug.security import safe_str_cmp 
""" The function safe_str_cmp will compare two strings but 
makes sure that in different python versions our program works as usual and not change because of possible 
ascii values difference in different os. """

def authenticate(username,password):
    user = UserModel.find_by_username(username)
    #If user exists and password is right return user like below.
    if user and safe_str_cmp(user.password,password):
        return user

#identity is a unique function in flask-jwt extension and the payload contains the content of jwt token
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)