from project.api.models import User, Company

def seedUser(db):
    db.session.add(User(username='Bernardohrl', email='bernardo@email.com', 
                    company_id='1', password='teste123'))
    db.session.add(User(username='Devsalula', email='saleh@email.com', 
                    company_id='2', password='teste123'))
    db.session.add(User(username='DuLtra', email='duLtra@email.com', 
                    company_id='3', password='teste123'))
    db.session.commit()


def seedCompany(db):
    db.session.add(Company(company_name='Loja1', cnpj='12312332', company_email='email1@email.com', 
                    fantasy_name='Lojinha1!', cep='32132112', city='Brasília', 
                    state='DF', company_phone='3344-2271'))
    db.session.add(Company(company_name='Loja2', cnpj='12312331', company_email='email2@email.com', 
                    fantasy_name='Lojinha2!', cep='32132112', city='Brasília', 
                    state='DF', company_phone='3344-2272'))
    db.session.add(Company(company_name='Loja3', cnpj='12312334', company_email='email3@email.com', 
                    fantasy_name='Lojinha3!', cep='32132112', city='Brasília', 
                    state='DF', company_phone='3344-2273'))
    db.session.commit()