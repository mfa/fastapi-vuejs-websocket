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

build+watch (with output in `app/dist`) with localhost setup
```
npm run watch
```

build (with output in `app/dist`) with production setup
```
npm run build
```

### deploy to fly.io

deploy:
```
npm run build
fly deploy --local-only
```
