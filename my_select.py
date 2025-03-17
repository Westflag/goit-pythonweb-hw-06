import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import db_models
from db_models import Student, Grade, Subject, Teacher, Group


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
async def select_1(session: AsyncSession):
    result = await session.execute(
        select(Student.name, func.avg(Grade.value).label("avg_score"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
    )
    return result.all()


# 2. Знайти студента із найвищим середнім балом з певного предмета
async def select_2(session: AsyncSession, subject_id: int):
    result = await session.execute(
        select(Student.name, func.avg(Grade.value).label("avg_score"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(1)
    )
    return result.first()


# 3. Знайти середній бал у групах з певного предмета
async def select_3(session: AsyncSession, subject_id: int):
    result = await session.execute(
        select(Group.name, func.avg(Grade.value).label("avg_score"))
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
    )
    return result.all()


# 4. Знайти середній бал на потоці (по всій таблиці оцінок)
async def select_4(session: AsyncSession):
    result = await session.execute(
        select(func.avg(Grade.value))
    )
    return result.scalar()


# 5. Знайти які курси читає певний викладач
async def select_5(session: AsyncSession, teacher_id: int):
    result = await session.execute(
        select(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
    )
    return result.all()


# 6. Знайти список студентів у певній групі
async def select_6(session: AsyncSession, group_id: int):
    result = await session.execute(
        select(Student.name)
        .filter(Student.group_id == group_id)
    )
    return result.all()


# 7. Знайти оцінки студентів у окремій групі з певного предмета
async def select_7(session: AsyncSession, group_id: int, subject_id: int):
    result = await session.execute(
        select(Student.name, Grade.value)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
    )
    return result.all()


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
async def select_8(session: AsyncSession, teacher_id: int):
    result = await session.execute(
        select(func.avg(Grade.value))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
    )
    return result.scalar()


# 9. Знайти список курсів, які відвідує певний студент
async def select_9(session: AsyncSession, student_id: int):
    result = await session.execute(
        select(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
    )
    return result.all()


# 10. Список курсів, які певному студенту читає певний викладач
async def select_10(session: AsyncSession, student_id: int, teacher_id: int):
    result = await session.execute(
        select(Subject.name)
        .join(Grade)
        .join(Teacher)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
    )
    return result.all()


DATABASE_URL = db_models.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def main():
    async with AsyncSessionLocal() as session:
        top_students = await select_1(session)
        print(top_students)


if __name__ == "__main__":
    asyncio.run(main())
