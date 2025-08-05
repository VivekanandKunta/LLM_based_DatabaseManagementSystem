from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from query_utils import generate_sql_query, extract_sql_content, run_query, get_schema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, set allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DBConfig(BaseModel):
    database: str
    user: str
    password: str
    host: str
    port: str

class QueryRequest(BaseModel):
    db_config: DBConfig
    sql_query: str

class PromptRequest(BaseModel):
    db_config: DBConfig
    prompt: str
    schema_text: str

@app.post("/generate-sql")
def generate_sql(request: PromptRequest):
    try:
        generated = generate_sql_query(request.schema_text, request.prompt)
        clean_sql = extract_sql_content(generated)
        print("Generated SQL:", clean_sql) 
        return { "generated_sql": clean_sql }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run-query")
def run_sql(request: QueryRequest):
    try:
        df = run_query(request.db_config, request.sql_query)
        print("📄 Query returned rows:", df.shape[0]) 
        print(df.head())  
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/get-schema")
def fetch_schema(request: QueryRequest):
    try:
        schema_text, schema_dict = get_schema(request.db_config)
        return { "schema_text": schema_text, "schema_dict": schema_dict }
    except Exception as e:
        print("Error while fetching schema:", str(e))  # 👈 Debug line
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/test-schema")
def test_schema():
    # hardcode your working config temporarily
    from pydantic import BaseModel

    class FakeConfig(BaseModel):
        database = "your_db_name"
        user = "your_user"
        password = "your_pass"
        host = "localhost"
        port = "5432"

    fake = FakeConfig()
    text, _ = get_schema(fake)
    return {"schema_text": text}
