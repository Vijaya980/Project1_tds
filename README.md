# Data Science Project

This project is a data science application that uses Docker for containerization.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Docker installed on your machine

### Building the Docker Image

To build the Docker image, run the following command in the project directory:

```sh
docker build -t llm-agent-project .
```

### Running the Docker Container

To run the Docker container, use the following command:

```sh
docker run -p 8000:8000 -e AIPROXY_TOKEN="$OPENAI_API_KEY"  llm-agent-project
```
or 
```sh
docker run -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY"  llm-agent-project
```

This will start the application and map port 8000 of the container to port 8000 on your local machine.

## Usage

Once the container is running, you can access the application by navigating to `http://localhost:8000` in your web browser.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
