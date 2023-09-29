import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apis import router

app = FastAPI()
app.include_router(router)

origins = ["*"]
laptop_ip = "127.0.0.1"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins  + [f"http://{laptop_ip}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)