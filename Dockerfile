FROM python:3.11-slim


WORKDIR /app


COPY . .


RUN pip install flask pandas matplotlib seaborn scikit-learn numpy joblib


EXPOSE 5000


CMD ["python", "app.py"]