from django.apps import AppConfig

print("start apps users")
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.users'
print("end apps users")
