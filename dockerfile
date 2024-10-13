FROM python:3

# Clone the repository
RUN git clone https://github.com/Hoinkas/DeafPolandStatistics.git

WORKDIR /home/vscode/DeafPolandStatistics/

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Specify the command to run the Python application
CMD ["python3", "app.py"]


