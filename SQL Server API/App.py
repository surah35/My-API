from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pymssql
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# globla 
SERVER = os.getenv("DB_SERVER")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DBNAME = "Virtual_Store"
TBNAME = "store_data"


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/data")
def get_data():
    try:
        conn = pymssql.connect(
            server=SERVER,
            charset='UTF-8',
            user=USER,
            password=PASSWORD,
            database=DBNAME,
        )
        
        if conn == None:
            return
        print("資料庫連接成功")

        cursor = conn.cursor(as_dict=True)
        cursor.execute(f"SELECT * FROM {TBNAME}")
        result = cursor.fetchall()
        cursor = conn.cursor(as_dict=False)
        cursor.execute(f"SELECT MAX(ID) as MaxID FROM {TBNAME}")
        maxid = cursor.fetchone()
        conn.close()
        return JSONResponse(content={"MaxID":maxid,"array":result})
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)