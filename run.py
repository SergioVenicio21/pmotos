from app import create_app
from app.controllers import user, brands

app = create_app()
app.register_blueprint(user.user_bp)
app.register_blueprint(brands.brand_bp)

if __name__ == '__main__':
    app.run()
