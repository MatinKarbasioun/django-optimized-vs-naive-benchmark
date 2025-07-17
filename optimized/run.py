import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "crm_optimized.asgi:application",
        host="127.0.0.1", port=8000,
        reload=True,
        log_level="info",
        workers=3,
        lifespan="off"
    )
    import uvicorn
