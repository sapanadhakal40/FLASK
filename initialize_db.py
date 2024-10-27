from app import db, app

with app.app_context():
    db.create_all()  # This will create the database and tables if they don't exist
    print("Database and tables created.")