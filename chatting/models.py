from django.db import models
from django.conf import settings


# Create your models here.

class Connection(models.Model):
    user1 = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE,
      related_name = "user1"
    )
    user2 = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE,
      related_name = "user2"
    )
    connection_id = models.CharField(max_length=200 )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.connection_id

    def get_or_create_room_id(user1 , user2):
        connection_obj = Connection.objects.filter(user1 = user1 , user2 = user2).first()
        if connection_obj:

            return connection_obj
        connection_obj = Connection.objects.filter(user1 = user2 , user2 = user1).first()
        if connection_obj:

            return connection_obj
        else:

            connection_id = str(user1.id) + str(user2.id)
            connection_obj = Connection.objects.create(user1 = user1 , user2 = user2 , connection_id = connection_id)
            connection_obj.save()
            return connection_obj



class Message(models.Model):
    connection = models.ForeignKey(
      Connection, 
      on_delete=models.CASCADE,
      related_name = "message"
    )
    sender = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE,
      related_name = "sender"
    )
    receiver = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      on_delete=models.CASCADE,
      related_name = "receiver"
    )
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message