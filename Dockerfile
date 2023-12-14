# Use the latest Ubuntu image for base image.
FROM ubuntu:latest

# Run a system update, install python3 and pip3.
RUN apt-get update && apt-get install python3 python3-pip -y

# Install ML packages and modules: jupyter, NumPy, Pandas, scikit-learn, matplotlib, plotly.
RUN pip3 install jupyter numpy pandas scikit-learn matplotlib plotly

# Install Flask.
RUN pip3 install flask

# Set the container to the working directory to a new folder for the app in root directory.
WORKDIR /app/han-karaoke-ml

COPY . .

# Ports to be exposed via docker-compose file.
EXPOSE 8888
EXPOSE 8080

# Start the Juptyer notebook server and Flask app.
ENTRYPOINT [ "sh", "./start-apps.sh" ]