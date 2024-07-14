# idifcy

Intelligent Design Implementation for Facilitating Construction Yields

## Setup

### Python part

```bash
pip install -r requirements.txt
```

### JS part

```bash
cd pages/frontend-viewer/
npm i
```

## Run

```bash
streamlit run Homepage.py
```

## Docker

```commandline
# Build Docker image
docker build -t idifcy .

# Run Docker container
docker run -p 8501:8501 idifcy
```

