import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app_local import app, db



migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=8080))


if __name__ == '__main__':
    manager.run()
