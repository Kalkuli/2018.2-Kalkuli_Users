from flask.cli import FlaskGroup
from project import app, db
from project.api.models import Company, User

cli = FlaskGroup(app)


# Registers new comand to recreate database
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()