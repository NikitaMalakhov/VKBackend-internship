from django.db import models
from django.db.models import UniqueConstraint


class User(models.Model):
    def __lt__(self: models.Model, other: models.Model):
        return self.id < other.id
    

    username = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"User #{self.id}: {self.username}"
    
    # class Meta:
    #     db_table = "users"
    #     db_table_comment = "Users table"




class FriendshipRequest(models.Model):
    addressee = models.ForeignKey(User, related_name='addressee', on_delete=models.CASCADE)
    destination = models.ForeignKey(User, related_name='destination', on_delete=models.CASCADE)


class Friendship(models.Model):
    user_1 = models.ForeignKey(User, related_name='user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='user_2', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_1', 'user_2',)
    
    def __str__(self) -> str:
        return f"Friendship #{self.id} : {self.user_1.username} <--> {self.user_2.username}"