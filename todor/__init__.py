from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# base de datos
db = SQLAlchemy()


# funcion de la creacionde la app
def create_app():

    app = Flask(__name__)

    # Configuracion del proyecto
    app.config.from_mapping(
        DEBUG=True,
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///todolist.db'
    )

    # Inicialzacion de la base de datos en la app

    db.init_app(app)

    # Blueprint
    from . import todo, auth
    app.register_blueprint(todo.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    # migracion de los modelos
    with app.app_context():
        db.create_all()

    return app
