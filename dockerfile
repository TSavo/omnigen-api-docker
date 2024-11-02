FROM python:3.11

# Set up working directory
WORKDIR /app

RUN apt update && apt install -y \
    git

# Install required Python packages
RUN pip install flask

# Clone the OmniGen repository and install it
RUN git clone https://github.com/staoxiao/OmniGen.git
RUN cd OmniGen \
    && pip install -e .

# Add the application code
COPY server.py /app
COPY firsttime.py /app

RUN pip uninstall torch torchvision torchaudio
RUN pip install torch torchvision torchaudio

RUN cd OmniGen && python3 ../firsttime.py

# Expose the port
EXPOSE 5000

# Set default command
CMD ["python3", "server.py"]

