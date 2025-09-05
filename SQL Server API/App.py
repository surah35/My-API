from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pymssql
from pydantic import BaseModel
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

class StoreItem(BaseModel):
    ID: int
    Name: str
    Price: int
    Num:int

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
    
# 新增資料
@app.post("/api/data")
def insert_data(item: StoreItem):
    try:
        conn = pymssql.connect(
            server=SERVER,
            charset='UTF-8',
            user=USER,
            password=PASSWORD,
            database=DBNAME,
        )
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {TBNAME} (ID, Name, Price, Num) VALUES (%s, %s, %s, %s)",
            (item.ID, item.Name, item.Price, item.Num)
        )
        conn.commit()
        conn.close()
        return JSONResponse(content={"message": "資料新增成功", "data": item.dict()})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# 刪除資料
@app.delete("/api/data/{id}")
def delete_data(id: int):
    try:
        conn = pymssql.connect(
            server=SERVER,
            charset='UTF-8',
            user=USER,
            password=PASSWORD,
            database=DBNAME,
        )
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TBNAME} WHERE ID = %s", (id,))
        conn.commit()
        conn.close()
        return JSONResponse(content={"message": f"ID {id} 已刪除"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)