import os
from flask_migrate import Migrate
from app.__init__ import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    port = 8000  # Porta de sua escolha
    app.run(host="0.0.0.0", port=port, debug=app.config.get('DEBUG', False))