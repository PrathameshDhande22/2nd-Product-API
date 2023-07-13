import uvicorn
from api import create_app

app=create_app()

if __name__=='__main__':
    uvicorn.run("run:app",reload=True,env_file=".env")