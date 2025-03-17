import asyncio
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import db_models
from db_models import Base, Student, Group, Teacher, Subject, Grade

# Підключення до бази даних PostgreSQL
DATABASE_URL = db_models.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
fake = Faker()


async def seed_db():
    async with AsyncSessionLocal() as session:
        # Створення груп
        groups = [Group(name=f"Group {i + 1}") for i in range(3)]
        session.add_all(groups)
        await session.commit()

        # Створення викладачів
        teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
        session.add_all(teachers)
        await session.commit()

        # Створення предметів
        subjects = [Subject(name=fake.word().capitalize(), teacher_id=random.choice(teachers).id) for _ in
                    range(random.randint(5, 8))]
        session.add_all(subjects)
        await session.commit()

        # Створення студентів
        students = [Student(name=fake.name(), group_id=random.choice(groups).id) for _ in range(random.randint(30, 50))]
        session.add_all(students)
        await session.commit()

        # Створення оцінок
        grades = []
        for student in students:
            for subject in subjects:
                for _ in range(random.randint(5, 20)):  # До 20 оцінок для кожного студента
                    grades.append(Grade(
                        student_id=student.id,
                        subject_id=subject.id,
                        value=random.randint(1, 10),
                        date_received=fake.date_this_year()
                    ))
        session.add_all(grades)
        await session.commit()

        print("✅ База даних успішно заповнена випадковими даними!")


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await seed_db()


if __name__ == "__main__":
    asyncio.run(main())
