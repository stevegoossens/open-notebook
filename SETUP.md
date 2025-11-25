# Setup

Copy example env file

```
cp .env.example docker.env
```

Edit `docker.env` to point at `ollama` container

```
OLLAMA_API_BASE="http://ollama:11434"
```

Start docker stack

```
docker compose -f docker-compose.full-with-ollama.yml up
```

Pull models

```
docker compose -f docker-compose.full-with-ollama.yml exec ollama bash
```

Download models inside container

```
ollama pull llama2
ollama pull mistral
ollama pull llama2:13b
```

Restart docker compose stack

```
# stop the running stack with Ctrl+C or `docker compose stop`
docker compose -f docker-compose.full-with-ollama.yml up -d
```
