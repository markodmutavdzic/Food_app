FROM python:3.8

WORKDIR /Food_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "recipes.py"]