from django.apps import AppConfig

print("pre app pc components")
class PcComponentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pc_components'
print("post app pc components")