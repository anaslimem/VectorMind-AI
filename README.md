# VectorMind AI: Your Personal Document Q&A Engine

VectorMind AI is a full-stack, AI-powered application that allows you to chat with your documents. Upload PDFs, text files, or paste raw text, and get intelligent, context-aware answers from a powerful language model.

This project is built with a modern, scalable, and cloud-native architecture, demonstrating a complete end-to-end workflow from development to deployment.

▶️ **[Link to your LinkedIn video demo here!]**

![Architecture Diagram](path/to/your/architecture_diagram.png)
*(Suggestion: Create a simple diagram and link it here)*

## ✨ Features

*   **Interactive Web UI**: A clean and user-friendly interface built with Streamlit.
*   **Multiple Ingestion Formats**: Supports PDF files, TXT files, and direct text input.
*   **Asynchronous Document Processing**: Uploads are handled by a background worker using a Redis message queue, ensuring the UI is always fast and responsive.
*   **Retrieval-Augmented Generation (RAG)**: Provides answers grounded in the context of your documents, reducing hallucinations.
*   **Persistent Knowledge**: Uses ChromaDB as a vector store to permanently save document knowledge.
*   **LLM Caching**: Implements a Redis cache for LLM responses to provide instant answers for repeated queries and reduce computational load.
*   **Cloud-Native & Scalable**: Fully containerized with Docker and orchestrated with Kubernetes for production-grade deployment.

## 🛠️ Tech Stack

### Application & AI
*   **Frontend**: [Streamlit](https://streamlit.io/ )
*   **Backend API**: [FastAPI](https://fastapi.tiangolo.com/ )
*   **AI Orchestration**: [LangChain](https://www.langchain.com/ )
*   **LLM Serving**: [Ollama](https://ollama.com/ )
*   **Vector Database**: [ChromaDB](https://www.trychroma.com/ )
*   **Message Queue & Caching**: [Redis](https://redis.io/ )
*   **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`

### Infrastructure & DevOps
*   **Containerization**: [Docker](https://www.docker.com/ )
*   **Orchestration**: [Kubernetes](https://kubernetes.io/ )
*   **Local Cluster**: [Minikube](https://minikube.sigs.k8s.io/docs/ )

## 🚀 Getting Started

There are two ways to run this project: locally using Docker Compose for development, or by deploying it to a Kubernetes cluster.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/ ) & [Docker Compose](https://docs.docker.com/compose/install/ )
*   [Kubernetes](https://kubernetes.io/docs/setup/ ) (e.g., via [Minikube](https://minikube.sigs.k8s.io/docs/start/ ) or Docker Desktop)
*   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/ )
*   [Ollama](https://ollama.com/ ) installed and running on your host machine.
*   Pull the required LLM model: `ollama pull <your_model_name>` (e.g., `ollama pull llama3`)

### 1. Running Locally with Docker Compose

This is the quickest way to get the application running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/vectormind-ai.git
    cd vectormind-ai
    ```

2.  **Configure Environment Variables:**
    The necessary environment variables are already set in the `docker-compose.yml` file to work with a local Ollama instance. Ensure Ollama is running on your host machine.

3.  **Build and run the application:**
    ```bash
    docker-compose up --build
    ```

4.  **Access the application:**
    *   **Streamlit Frontend**: Open your browser and go to `http://localhost:8501`
    *   **FastAPI Backend Docs**: `http://localhost:8000/docs`

### 2. Deploying to Kubernetes

This section guides you through deploying the application to a Kubernetes cluster.

1.  **Ensure your Kubernetes cluster is running.**
    ```bash
    minikube start
    ```

2.  **Build and Push Docker Images:**
    You must build the `frontend` and `backend` images and push them to a public container registry like Docker Hub.
    ```bash
    # Replace 'your-dockerhub-username' with your actual username
    docker build -t your-dockerhub-username/vectormind-ai-backend:latest ./backend
    docker push your-dockerhub-username/vectormind-ai-backend:latest

    docker build -t your-dockerhub-username/vectormind-ai-frontend:latest ./frontend
    docker push your-dockerhub-username/vectormind-ai-frontend:latest
    ```

3.  **Update Kubernetes YAML files:**
    In the `k8s/` directory, update the `*-deployment.yml` files to use the image names you just pushed. You also need to configure the `OLLAMA_BASE_URL` to point to your host machine's IP address accessible from within the cluster.

    *Example in `k8s/backend-deployment.yml`:*
    ```yaml
    # ...
    spec:
      containers:
      - name: backend
        image: your-dockerhub-username/vectormind-ai-backend:latest
        env:
        - name: OLLAMA_BASE_URL
          value: "http://<your-host-ip>:11434" # Find your IP accessible from Minikube
    # ...
    ```

4.  **Apply the Kubernetes configurations:**
    Navigate to the `k8s` directory and apply all the YAML files.
    ```bash
    cd k8s
    kubectl apply -f .
    ```

5.  **Verify the deployment:**
    Check that all pods are in the `Running` state.
    ```bash
    kubectl get pods
    ```

6.  **Access the application:**
    Find the external IP for the frontend service and open it in your browser.
    ```bash
    # If using Minikube, run this in a separate terminal
    minikube service frontend-service
    ```
    This will automatically open the application in your browser.

## 🏛️ Architecture Overview

*   **Frontend (`streamlit/` )**: The user-facing web application.
*   **Backend (`backend/`)**: The FastAPI application containing the core API logic.
    *   `routers/`: Defines the API endpoints for querying and ingestion.
    *   `utils/`: Contains helper functions for connecting to Redis, ChromaDB, and initializing the LLM.
    *   `worker.py`: The background worker that consumes jobs from the Redis Stream for document processing.
*   **Dockerfiles**: Each service (`frontend`, `backend`) has its own Dockerfile for containerization.
*   **`docker-compose.yml`**: Defines the multi-container setup for local development.
*   **Kubernetes (`k8s/`)**: Contains all the YAML manifests for deploying the application to a Kubernetes cluster.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/limemanas/vectormind-ai/issues ).