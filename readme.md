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

build (with output in `app/dist`)
```
npm run build
```

build+watch (with output in `app/dist`)
```
npm run watch
```


### deploy to fly.io

deploy:
```
npm run build
fly deploy --local-only
```
