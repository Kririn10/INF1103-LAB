FROM python:3.11-slim
WORKDIR /app
COPY inventory_manager_OOP.py .
CMD ["python", "-u", "inventory_manager_OOP.py"]