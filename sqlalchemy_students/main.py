from sqlalchemy import String, create_engine, select, and_, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column()


engine = create_engine("sqlite:///students.db")
Base.metadata.create_all(engine)


def search_students(session, min_age, max_age, part):
    statement = select(Student).where(
        and_(
            Student.age >= min_age,
            Student.age <= max_age,
            Student.name.ilike(f"%{part}%")
        )
    )
    return session.scalars(statement).all()


with Session(engine) as session:
    if session.query(Student).count() == 0:
        session.add_all([
            Student(name="Али", age=17),
            Student(name="Амина", age=19),
            Student(name="Дамир", age=20),
            Student(name="Марат", age=21),
            Student(name="Саша", age=16),
        ])
        session.commit()

    print("1. Младше 18:")
    print(session.scalars(select(Student).where(Student.age < 18)).all())

    print("\n2. Старше 18:")
    print(session.scalars(select(Student).where(Student.age > 18)).all())

    print("\n3. От 17 до 20 включительно:")
    print(session.scalars(
        select(Student).where(and_(Student.age >= 17, Student.age <= 20))
    ).all())

    print("\n4. Али или Амина:")
    print(session.scalars(
        select(Student).where(or_(Student.name == "Али", Student.name == "Амина"))
    ).all())

    print("\n5. Дамир или Марат:")
    print(session.scalars(
        select(Student).where(Student.name.in_(["Дамир", "Марат"]))
    ).all())

    print("\n6. В имени есть буква «а» без учёта регистра:")
    print(session.scalars(
        select(Student).where(Student.name.ilike("%а%"))
    ).all())

    print("\nДополнительно: возраст от 17 до 20, в имени есть «а»:")
    print(search_students(session, 17, 20, "а"))