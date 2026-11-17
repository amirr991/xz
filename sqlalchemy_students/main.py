from sqlalchemy import String, create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column()
    city: Mapped[str] = mapped_column(String(100))


engine = create_engine("sqlite:///student.db")
Base.metadata.create_all(engine)


def show_statistics(session):
    total = session.scalar(select(func.count(Student.id)))
    average_age = session.scalar(select(func.avg(Student.age)))
    min_age = session.scalar(select(func.min(Student.age)))
    max_age = session.scalar(select(func.max(Student.age)))
    total_age = session.scalar(select(func.sum(Student.age)))

    print("Количество студентов:", total)
    print("Средний возраст:", average_age)
    print("Минимальный возраст:", min_age)
    print("Максимальный возраст:", max_age)
    print("Сумма возрастов:", total_age)


def count_by_city(session, city):
    statement = select(func.count(Student.id)).where(Student.city == city)
    return session.scalar(statement)


with Session(engine) as session:
    if session.scalar(select(func.count(Student.id))) == 0:
        session.add_all([
            Student(name="Али", age=17, city="Атырау"),
            Student(name="Амина", age=19, city="Алматы"),
            Student(name="Дамир", age=17, city="Атырау"),
            Student(name="Марат", age=21, city="Астана"),
            Student(name="Саша", age=16, city="Атырау"),
        ])
        session.commit()

    show_statistics(session)

    count_17 = session.scalar(
        select(func.count(Student.id)).where(Student.age == 17)
    )
    print("Студентов 17 лет:", count_17)

    average_atyrau = session.scalar(
        select(func.avg(Student.age)).where(Student.city == "Атырау")
    )
    print("Средний возраст студентов из Атырау:", average_atyrau)

    print("Студентов из Атырау:", count_by_city(session, "Атырау"))