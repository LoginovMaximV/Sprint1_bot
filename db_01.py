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
p2 = User(2, "Логинов Максим", 89612594865, '1')
p3 = User(3, "Варова Ангелина", 89523641213, '1')
p4 = User(4, "Шпилевая Арина", 89082351698, '1')
p5 = User(5, "Григорьев Константин", 89031030066, '1')
p6 = User(6, "Кушнеров Иван", 89326549817, '0')
p7 = User(7, "Мезенцев Семён", 89519320462, '0')

session.add(p1)
session.add(p2)
session.add(p3)
session.add(p4)
session.add(p5)
session.add(p6)
session.add(p7)
session.commit()

class Application(Base):
    __tablename__ = "applications"

    id = Column("id заявки", Integer, primary_key=True)
    app = Column("Заявка", String)
    status = Column("Статус заявки", String)

    users_id = Column(Integer, ForeignKey('users.id'))

    chief = Column("Ответственны за исполнение", String)
    start = Column("Начало исполнения", String)
    stop = Column("Конец исполнения", String)

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


engins = create_engine("postgresql://postgres:938271@localhost/postgres", echo=True)
Base.metadata.create_all(bind=engins)

Session = sessionmaker(bind=engins)
session = Session()


a1 = Application(1, "Подбор земельного участка для строительства дома", "Принята", p2.id, "Агапов Алексей М.", "02.02.2024", "18.02.2024")
a2 = Application(2, "Юридическое сопровождение сделки с недвижимостью", "В разработке", p5.id, "Гневышев Денис И.", "25.01.2024", "10.02.2024")
a3 = Application(3, "Страхование недвижимости", "Выполнена", p4.id, "Свиридов Роман Р.", "05.02.2024", "15.02.2024")
a4 = Application(4, "Продажа квартиры", "Принята", p1.id, "Тимофеев Сергей Н.", "23.01.2024", "26.06.2024")
a5 = Application(5, "Оценка стоимости недвижимости", "В разработке", p3.id, "Сергеев Анатолий Л.", "02.02.2024", "18.02.2024")

session.add(a1)
session.add(a2)
session.add(a3)
session.add(a4)
session.add(a5)
session.commit()
