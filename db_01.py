from sqlalchemy import create_engine, ForeignKey, Column, String, BigInteger, Integer, text, Boolean, UUID
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
        new_user = User(name=name, email=email, status="active", number=number, admin=admin, vip=vip)
        session.add(new_user)
        session.commit()

engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()

# p1 = User("Пименова Татьяна", "Tatyana.pimenova@mail.ru", True, "+79512640239", False, False)
# p2 = User("Логинов Максим", "Maksim.loginov@mail.ru", True, "+79091894043", True, False)
# p3 = User("Варова Ангелина", "Angelina.varova@mail.ru", True, "+79058500627", True, True)
# p4 = User("Шпилевая Арина", "Arina.shpilevay@mail.ru", True, "+79129061392", False, False)
# p5 = User("Григорьев Константин", "Konstantin.grigoryev!mail.ru", True, "+79512757367", False, True)
# p6 = User("Кушнеров Иван", "Ivan.kushnerov@mail.ru", False, "+79326549817", False, False)
# p7 = User("Мезенцев Семён", "Cemen.mezencev@mail.ru", True, "+79322009131", False, False)
#
# session.add(p1)
# session.add(p2)
# session.add(p3)
# session.add(p4)
# session.add(p5)
# session.add(p6)
# session.add(p7)
session.expire_on_commit = False
session.commit()
connections.close()

class Application(Base):
    __tablename__ = "application"

    id = Column("application_id", Integer, primary_key=True)
    app = Column("application", String)
    status = Column("status_application", String)

    users_id = Column(UUID, ForeignKey('users.id'))

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


# a1 = Application(1, "Подбор земельного участка для строительства дома", "Принята", p2.id, "Агапов Алексей М.", "02.02.2024", "18.02.2024")
# a2 = Application(2, "Юридическое сопровождение сделки с недвижимостью", "В разработке", p5.id, "Гневышев Денис И.", "25.01.2024", "10.02.2024")
# a3 = Application(3, "Страхование недвижимости", "Выполнена", p4.id, "Свиридов Роман Р.", "05.02.2024", "15.02.2024")
# a4 = Application(4, "Продажа квартиры", "Принята", p1.id, "Тимофеев Сергей Н.", "23.01.2024", "26.06.2024")
# a5 = Application(5, "Оценка стоимости недвижимости", "В разработке", p3.id, "Сергеев Анатолий Л.", "02.02.2024", "18.02.2024")
#
# session.add(a1)
# session.add(a2)
# session.add(a3)
# session.add(a4)
# session.add(a5)
session.commit()
connections.close()


class Buttons(Base):
    __tablename__ = "button"

    id_category = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column("category", String)

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return f"({self.category})"

    def save_problem_to_db(category):
        new_category = Buttons(category=category)
        session.add(new_category)
        session.commit()

    @staticmethod
    def get_all_category():
        categorys = session.query(Buttons).all()
        return [category.category for category in categorys]





engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()

# b1 = Buttons("Интернет")
# b2 = Buttons("Документооборот")
# b3 = Buttons("Другое")
#
# session.add(b1)
# session.add(b2)
# session.add(b3)

session.expire_on_commit = False
session.commit()
connections.close()


class Problems(Base):
    __tablename__ = "problem"

    id_pr = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_category_pr = Column(UUID, ForeignKey('button.id'))
    problem = Column("problem", String)

    def __init__(self, id_category_pr, problem):
        self.id_category_pr=id_category_pr
        self.problem = problem

    def __repr__(self):
        return f"({self.id_category_pr}, {self.problem})"

    def save_problem_to_db(id_category_pr, problem):
        new_problem = Problems(id_category_pr=id_category_pr, problem=problem)
        session.add(new_problem)
        session.commit()

    @staticmethod
    def get_all_problems():
        problems = session.query(Buttons).all()
        return [problem.problem for problem in problems]





engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()

# b1 = Problems('837f8824-1077-4582-82cc-c1cfba6ab7b2', "Проблема 1")
# b2 = Problems('837f8824-1077-4582-82cc-c1cfba6ab7b2', "Проблема 2")
# b3 = Problems('837f8824-1077-4582-82cc-c1cfba6ab7b2', "Проблема 3")
#
# session.add(b1)
# session.add(b2)
# session.add(b3)

session.expire_on_commit = False
session.commit()
connections.close()

def user_exist(contact_number):
    q = session.query(User.number).filter(User.number == contact_number)
    return session.query(q.exists()).scalar()

def user_status(contact_number):
    g = session.query(User.status).filter(User.number == contact_number).first()
    return g