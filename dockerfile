FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y; apt-get upgrade -y

# Clone the repository
RUN git clone https://github.com/Hoinkas/DeafPolandStatistics.git
COPY ./ ./

# Install Python dependencies
RUN pip install -r requirements.txt

EXPOSE 8000

# Specify the command to run the Python application
CMD ["python3", "app.py"]


