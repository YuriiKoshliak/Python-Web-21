
import mongoengine as me

# Підключення до бази даних MongoDB
me.connect(host="mongodb+srv://***************")

class Contact(me.Document):
    fullname = me.StringField(required=True)
    email = me.StringField(required=True)
    message_sent = me.BooleanField(default=False)
    additional_info = me.StringField()
