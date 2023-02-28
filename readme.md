## fastapi-vuejs-websocket

testbed for experiments with fastapi + websockets with a vuejs frontend

### backend

run fastapi
```
uvicorn app.main:app --reload
```


### frontend

```
cd frontend
npm install
npm run dev
```

build:
```
npm run build
```


### deploy to fly.io

deploy:
```
fly deploy --local-only
```
