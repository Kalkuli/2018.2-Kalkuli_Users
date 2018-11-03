from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Company, User
import unittest
import coverage


# Config coverage report
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()


cli = FlaskGroup(create_app)


# Registers comand to recreate database
@cli.command()
def recreatedb():
    db.drop_all()
    db.create_all()
    db.session.commit()


# Registers comand to run tests
@cli.command()
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


# Registers command to get coverage
@cli.command()
def cov():
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.xml_report()
        return 0
    return 1



if __name__ == '__main__':
    cli()