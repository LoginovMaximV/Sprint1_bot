from sqlalchemy import create_engine, ForeignKey, Column, String, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("ФИО", String)
    number = Column("Номер телефона", BigInteger)
    status = Column("Статус", String)

    def __init__(self, id, name, number, status):
        self.id = id
        self.name = name
        self.number = number
        self.status = status

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.number}, {self.status})"


engin = create_engine("postgresql://postgres:938271@localhost/postgres", echo=True)
Base.metadata.create_all(bind=engin)

Session = sessionmaker(bind=engin)
session = Session()

p1 = User(1, "Пименова Татьяна", 89512640239, '1')
p2 = User(2, "Логинов Максим", 89512640239, '1')
p3 = User(3, "Варова Ангелина", 89512640239, '1')
p4 = User(4, "Шпилевая Арина", 89512640239, '1')
p5 = User(5, "Григорьев Константин", 89512640239, '1')
p6 = User(6, "Кушнеров Иван", 89512640239, '0')
p7 = User(7, "Мезенцев Семён", 89512640239, '0')

session.add(p1)
session.add(p2)
session.add(p3)
session.add(p4)
session.add(p5)
session.add(p6)
session.add(p7)
session.commit()
