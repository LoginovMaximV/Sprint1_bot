from sqlalchemy import create_engine, ForeignKey, Column, String, BigInteger, Integer, text, UUID, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("name", String)
    email = Column("email", String)
    status = Column("status", Boolean)
    number = Column("phone_number", String)
    admin = Column("is_admin", Boolean)
    vip = Column("is_vip", Boolean)


    def __init__(self, name, email, status, number, admin, vip):
        self.name = name
        self.email = email
        self.status = status
        self.number = number
        self.admin = admin
        self.vip = vip

    def __repr__(self):
        return f"({self.name}, {self.email}, {self.status}, {self.number}, {self.admin}, {self.vip})"

    def save_user_to_db(name, email, status, number, admin, vip):
        new_user = User(name=name, email=email, status=status, number=number, admin=admin, vip=vip)
        session.add(new_user)
        session.commit()

engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()

session.expire_on_commit = False
session.commit()
connections.close()

class Application(Base):
    __tablename__ = "application"

    id = Column("application_id", Integer, primary_key=True)
    app = Column("application", String)
    status = Column("status_application", String)

    users_id = Column(Integer, ForeignKey('userss.id'))

    chief = Column("responsible_execution", String)
    start = Column("start_execution", String)
    stop = Column("end_execution", String)

    def __init__(self, id, app, status, users_id, chief, start, stop):
        self.id = id
        self.app = app
        self.status = status
        self.users_id = users_id
        self.chief = chief
        self.start = start
        self.stop = stop

    def __repr__(self):
        return f"({self.id}, {self.app}, {self.status}, {self.users_id}, {self.chief}, {self.start}, {self.stop}"


engins = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engins.connect()


Base.metadata.create_all(bind=engins)

Session = sessionmaker(bind=engins)
session = Session()


#a1 = Application(1, "Подбор земельного участка для строительства дома", "Принята", p2.id, "Агапов Алексей М.", "02.02.2024", "18.02.2024")
#a2 = Application(2, "Юридическое сопровождение сделки с недвижимостью", "В разработке", p5.id, "Гневышев Денис И.", "25.01.2024", "10.02.2024")
#a3 = Application(3, "Страхование недвижимости", "Выполнена", p4.id, "Свиридов Роман Р.", "05.02.2024", "15.02.2024")
#a4 = Application(4, "Продажа квартиры", "Принята", p1.id, "Тимофеев Сергей Н.", "23.01.2024", "26.06.2024")
#a5 = Application(5, "Оценка стоимости недвижимости", "В разработке", p3.id, "Сергеев Анатолий Л.", "02.02.2024", "18.02.2024")

#session.add(a1)
#session.add(a2)
#session.add(a3)
#session.add(a4)
#session.add(a5)
#session.commit()
#connections.close()


class Category(Base):
    __tablename__ = "category"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"({self.id}, {self.name})"

    def save_name_to_db(id, name):
        new_name = Category(id=id, name=name)
        session.add(new_name)
        session.commit()

    @staticmethod
    def get_all_name():
        categorys = session.query(Category).all()
        return [name.name for name in categorys]





engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()


session.expire_on_commit = False
session.commit()
connections.close()

def user_exist(contact_number):
    q = session.query(User.number).filter(User.number == contact_number)
    return session.query(q.exists()).scalar()

def user_status(contact_number):
    g = session.query(User.status).filter(User.number == contact_number).first()
    return g