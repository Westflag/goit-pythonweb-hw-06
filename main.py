import argparse
import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from db_models import Group, Teacher, Subject, Student, Grade

async def create(session: AsyncSession, model, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    await session.commit()
    print(f"✅ {model.__name__} створено: {obj}")

async def list_all(session: AsyncSession, model):
    result = await session.execute(select(model))
    records = result.scalars().all()
    if not records:
        print(f"⚠️ У таблиці {model.__tablename__} немає записів.")
    else:
        print(f"\n📋 Список {model.__tablename__}:")
        for record in records:
            print(f"   {record}")


async def update(session: AsyncSession, model, id, **kwargs):
    obj = await session.get(model, id)
    if obj:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await session.commit()
        print(f"✅ {model.__name__} оновлено: {obj}")
    else:
        print(f"❌ {model.__name__} з ID {id} не знайдено.")

async def remove(session: AsyncSession, model, id):
    obj = await session.get(model, id)
    if obj:
        await session.delete(obj)
        await session.commit()
        print(f"✅ {model.__name__} видалено.")
    else:
        print(f"❌ {model.__name__} з ID {id} не знайдено.")

async def main():
    parser = argparse.ArgumentParser(description="CLI програма для роботи з БД школи")

    parser.add_argument("-a", "--action", choices=["create", "list", "update", "remove"], required=True, help="CRUD операція")
    parser.add_argument("-m", "--model", choices=["Group", "Teacher", "Subject", "Student", "Grade"], required=True, help="Модель")

    parser.add_argument("-id", type=int, help="ID для оновлення або видалення")
    parser.add_argument("-n", "--name", type=str, help="Ім'я")
    parser.add_argument("--group_id", type=int, help="ID групи")
    parser.add_argument("--teacher_id", type=int, help="ID викладача")
    parser.add_argument("--subject_id", type=int, help="ID предмета")
    parser.add_argument("--student_id", type=int, help="ID студента")
    parser.add_argument("--value", type=int, help="Оцінка")

    args = parser.parse_args()
    async with AsyncSessionLocal() as session:
        model_map = {
            "Group": Group,
            "Teacher": Teacher,
            "Subject": Subject,
            "Student": Student,
            "Grade": Grade
        }
        model = model_map[args.model]

        if args.action == "create":
            data = {k: v for k, v in vars(args).items() if v is not None and k not in ["action", "model", "id"]}
            await create(session, model, **data)

        elif args.action == "list":
            await list_all(session, model)

        elif args.action == "update":
            if args.id:
                data = {k: v for k, v in vars(args).items() if v is not None and k not in ["action", "model", "id"]}
                await update(session, model, args.id, **data)
            else:
                print("❌ Потрібно вказати --id для оновлення.")

        elif args.action == "remove":
            if args.id:
                await remove(session, model, args.id)
            else:
                print("❌ Потрібно вказати --id для видалення.")

if __name__ == "__main__":
    asyncio.run(main())
