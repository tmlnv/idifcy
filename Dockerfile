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

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install JavaScript dependencies
# Ensure you run npm install as 'pn' user to avoid permission issues
RUN npm install --prefix pages/frontend-viewer/

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Switch back to the 'pn' user
USER pn

# Run streamlit when the container launches
CMD ["streamlit", "run", "Homepage.py"]
