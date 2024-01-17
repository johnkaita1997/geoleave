FROM python:3.9.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /code

# Copy only the requirements file to the working directory
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv venv
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["venv/bin/python", "geoleave/manage.py", "runserver", "0.0.0.0:8000"]
