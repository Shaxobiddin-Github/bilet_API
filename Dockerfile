# Asosiy Python imidjidan foydalanamiz
FROM python:3.11-slim

# Ishchi direktoriyani belgilaymiz
WORKDIR /app

# Loyiha talablarini nusxalaymiz va o'rnatamiz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini konteynerga nusxalaymiz
COPY . .
RUN python manage.py collectstatic --noinput
# Portni ochamiz (odatiy 8000)
EXPOSE 8000

# Gunicorn bilan serverni ishga tushiramiz
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bace.wsgi:application"]