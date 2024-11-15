from rest_framework import serializers
from models import User, Table, Organization

class UserSerializer(serializers.ModelSerializer):
  user = User
  def get(self, user_id):
    if self.user.telegram_id == user_id:
      return self.user.telegram_id
    
  # def getOrganition(self):
  #   organization = Organization
  #   return self.organization.title
    
