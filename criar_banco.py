from fekepinterest import database, app
from fekepinterest.models import*

with app.app_context():
    database.create_all()