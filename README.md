# idifcy

Intelligent Design Implementation for Facilitating Construction Yields (idifcy)
is a robust tool designed to streamline the validation and visualization of IFC files
using innovative IDS technology. It enhances the quality assurance processes
in construction projects through IDS validation and verification.

## Setup

### Python part

To install the necessary Python dependencies:

```bash
poetry install
```

### JS part

For setting up the JavaScript environment, particularly for the frontend viewer:

```bash
cd pages/frontend-viewer/
npm install
```

## Run

To start the application with Streamlit:

```bash
streamlit run Homepage.py
```

## Docker

You can use Docker to build and run idifcy as follows:

```commandline
# Build Docker image
docker build -t idifcy .

# Run Docker container
docker run -p 8501:8501 idifcy
```

### DockerHub

Due to a dependency on a specific version of `ifcopenshell`
that is not available on PyPI,
the current working build of idifcy is only available through DockerHub.

You can pull the latest image directly from DockerHub:

```commandline
docker pull tmlnv/idifcy:latest
```
