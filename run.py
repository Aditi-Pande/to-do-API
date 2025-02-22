from app import create_app
from app.routes import routes
from app.database import db_connection

app = create_app()

app.register_blueprint(routes)

if __name__ == "__main__":
    db_connection(app)
    app.run(host="0.0.0.0", debug=True)
