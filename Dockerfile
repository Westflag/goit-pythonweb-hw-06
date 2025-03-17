FROM python:3.11

# Встановлення робочої директорії
WORKDIR /app

# Копіюємо файли проєкту у контейнер
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Оголошуємо змінні середовища
ENV DATABASE_URL=postgresql+asyncpg://user:password@db:5432/school

# Запускаємо додаток
CMD ["python", "main.py"]
