from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pymssql

app = FastAPI()

# SQL Server 連線字串
SERVER = "127.0.0.1"
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
            database=DBNAME,
        )
        return {"Hello": "World"}
        if conn == None:
            return
        print("資料庫連接成功")

        cursor = conn.cursor(as_dict=True)
        cursor.execute(f"SELECT TOP 5 * FROM {TBNAME}")
        
        result = cursor.fetchall()
        conn.close()
        return JSONResponse(content=result)
        
    except pymssql.DatabaseError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    


    # try:
    #     conn = pyodbc.connect(conn_str)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT TOP 5 * FROM YourTable")
    #     rows = cursor.fetchall()
    #     result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    #     conn.close()
    #     return jsonify(result)
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)