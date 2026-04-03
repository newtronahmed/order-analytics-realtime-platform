from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
import ksql
import time
import asyncio

app = FastAPI()

# KSQLDB Configuration
KSQLDB_URL = 'http://localhost:8088'
ksql_client = ksql.KSQLAPI(KSQLDB_URL)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    await initialize_ksqldb()

async def initialize_ksqldb():
    try:
        # Create stream or table if not exists
        await ksql_client.execute("CREATE STREAM orders_stream (order_id INT, amount FLOAT) WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON');")
    except Exception as e:
        print(f"Error initializing ksqlDB: {e}")

@app.get("/query/{query_id}")
async def query_ksqldb(query_id: str):
    try:
        result = await ksql_client.query(f"SELECT * FROM orders_stream EMIT CHANGES;")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sse/orders")
async def sse_orders():
    async def event_generator():
        while True:
            data = await query_ksqldb("orders")
            yield f"data: {data}\n\n"
            await asyncio.sleep(1)  # Adjust as needed to control frequency of events
    return StreamingResponse(event_generator(), media_type="text/event-stream")
