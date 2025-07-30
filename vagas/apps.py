from django.apps import AppConfig


class VagasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vagas'
    
    def ready(self):
        """
        Importa os signals quando a aplicação é carregada
        """
        import vagas.signals
