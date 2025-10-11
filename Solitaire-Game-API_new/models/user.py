from google.cloud import ndb


class User(ndb.Model):
    """User profile"""
    user_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
