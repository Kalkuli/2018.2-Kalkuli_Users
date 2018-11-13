import coverage
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Company, User
from project.tests.utils import add_company
import unittest


# Config coverage report

app = create_app()
cli = FlaskGroup(app)


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

@cli.command()
def seeduserdb():
    company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
    db.session.add(User(
        username='michael',
        email='michael@reallynotreal.com',
        password='greaterthaneight',
        company_id=company.id
    ))
    company_two = add_company('Kalkuli', '00.000.000/0000-00', 'kli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
    db.session.add(User(
        username='michaelherman',
        email='michael@mherman.org',
        password='greaterthaneight',
        company_id=company_two.id
    ))
    db.session.commit()

if __name__ == '__main__':
    cli()