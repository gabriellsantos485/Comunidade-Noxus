from comunidade_noxus import database, app
from comunidade_noxus.models import Usuario

with app.app_context():
    user=Usuario.query.first()
    print("A senha do usuario é:",user.senha)