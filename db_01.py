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

    @staticmethod
    def get_admin_status(phone):
        admin_st = session.query(User).filter(User.number == phone).first()
        return admin_st.admin


engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()

session.expire_on_commit = False
session.commit()
connections.close()


class Problem(Base):
    __tablename__ = "service_category"

    id = Column("id", Integer, primary_key=True)
    id_category = Column(Integer, ForeignKey('category.id'))
    name = Column("name", String)

    def __init__(self, id, id_category, name):
        self.id = id
        self.id_category = id_category
        self.name = name

    def __repr__(self):
        return f"({self.id}, {self.id_category}, {self.name}"

    @staticmethod
    def get_all_problems():
        problems = session.query(Problem).all()
        return [problem.problem for problem in problems]

    @staticmethod
    def get_names_by_id(prob_id):
        names = []
        categories = session.query(Problem).filter(Problem.id_category == prob_id).all()
        for category in categories:
            names.append(category.name)
        return names

    @staticmethod
    def get_id_by_name(problem_name):
        problem = session.query(Problem).filter(Problem.name == problem_name).first()
        if problem is not None:
            return problem.id
        else:
            return None

    @staticmethod
    def get_name_by_id(prob_id):
        problem = session.query(Problem).filter(Problem.id == prob_id).first()
        if problem is not None:
            return problem.name
        else:
            return None

engins = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engins.connect()


Base.metadata.create_all(bind=engins)

Session = sessionmaker(bind=engins)
session = Session()

session.commit()
connections.close()


class Application(Base):
    __tablename__ = "application"

    id = Column("application_id", Integer, primary_key=True)
    app = Column("application", String)
    status = Column("status_application", String)

    users_id = Column(Integer, ForeignKey('users.id'))

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
        categories = session.query(Category).all()
        return [name.name for name in categories]

    @staticmethod
    def get_id_by_name(category_name):
        category = session.query(Category).filter(Category.name == category_name).first()
        if category:
            return category.id
        else:
            return None


engin = create_engine('postgresql://st3:/XjHt(~_+iiRLKPgZvFA;q%5$WhCfW@37.18.110.244:5432/helpDesk')

connections = engin.connect()

Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()
session.expire_on_commit = False
session.commit()
connections.close()


class Problems(Base):
    __tablename__ = "problem"

    id_pr = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #id_category_pr = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    id_category_pr = Column(Integer, ForeignKey('category.id'))
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