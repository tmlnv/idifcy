FROM nikolaik/python-nodejs:python3.11-nodejs20-slim

# Switch to root to perform installations
USER root

WORKDIR /home/pn/app

# Confirm node, npm, and python installations
RUN node --version
RUN npm --version
RUN python --version

# Copy the current directory contents into the container at /app
COPY . /home/pn/app

# Change ownership of the copied files to the 'pn' user
RUN chown -R pn:pn /home/pn/app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry and Python binaries are in PATH
ENV PATH="/root/.local/bin:$PATH"

# Disable virtualenv creation from poetry to use the system python
ENV POETRY_VIRTUALENVS_CREATE=false

# gcc for building deps
RUN apt-get update && apt-get install -y gcc libpython3-dev

# Install dependencies
RUN poetry install --no-interaction --no-ansi -vv --no-root

# Install JavaScript dependencies
# Ensure you run npm install as 'pn' user to avoid permission issues
RUN npm install --prefix pages/frontend-viewer/

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Switch back to the 'pn' user
USER pn

# Run streamlit when the container launches
CMD ["streamlit", "run", "Homepage.py"]
