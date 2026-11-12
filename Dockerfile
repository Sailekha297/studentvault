FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN groupadd --system --gid 10001 appuser \
    && useradd --system --uid 10001 --gid 10001 \
       --home-dir /home/appuser --create-home appuser \
    && chown -R appuser:appuser /app

USER 10001:10001

EXPOSE 8000

CMD ["gunicorn", "student_portfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]