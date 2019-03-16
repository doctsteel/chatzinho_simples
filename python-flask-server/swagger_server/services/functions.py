from sqlalchemy import func
from ..models.database import UserList, MessageDb

class ServidorChat:
    def __init__(self):
        pass

    def accept_connection(self, user):
        new_user = UserList()
        new_user.username = user
        db_session.add(new_user)
        db_session.commit()
        result = "New user added to the database", 200
        return result

    def close_connection(self, user):
        quitting_user = db_session.query(UserList).filter(Userlist.username=user).one()
        db_session.delete(user)        
        result = "User removed from database", 200
        return result

    def broadcast_message(self, message):
        

    def receive_message(self, message):
        
