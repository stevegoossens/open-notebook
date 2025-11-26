# Setup

## Copy example env file

```
cp .env.example docker.env
```

## Use `sed` to replace the OLLAMA_API_BASE line:

```
sed -i 's|^# OLLAMA_API_BASE=.*$|OLLAMA_API_BASE="http://ollama:11434"|' docker.env
```

<details><summary>Manual way: expand/collapse</summary><p>

Edit `docker.env` to point at `ollama` container

```
OLLAMA_API_BASE="http://ollama:11434"
```

</p></details>

## Start docker stack

```
docker compose up -d
```

<details><summary>Pull different models: expand/collapse</summary><p>

Pull models

```
docker compose exec ollama bash
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
docker compose up -d
```

</p><details>
