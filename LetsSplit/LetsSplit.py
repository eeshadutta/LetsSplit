from flask import Flask
from config import dev_config
from models import DB
from controllers import app_blueprint


app = Flask(__name__)
app.config.from_object(dev_config)

app.register_blueprint(app_blueprint)

if __name__ == '__main__':
    DB.init_app(app=app)
    DB.create_all(app=app)
    app.run()
