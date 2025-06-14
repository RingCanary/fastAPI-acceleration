import asyncio
import time

from contextlib import asynccontextmanager
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI, Request
import httpx

import numpy as np
from numba import jit
import aiofiles

# setup context manager lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # create a single reusable process pool
    app.state.executor = ProcessPoolExecutor()
    yield

    app.state.executor.shutdown()

# setup the fastapi app

app = FastAPI(lifespan=lifespan)

## --- core functions to test and optimize

# testing write I/O
async def save_to_file_async(filename: str):
    async with aiofiles.open(filename, mode='w') as f:
        await asyncio.sleep(1) # well this simulates a slow disk or floppy write
        await f.write(f"Completed at {time.time()}")
    return f"Written to {filename}"

## --- api endpoints
@app.get("/")
def read_root():
    return {"message": "Hello from the FastAPI testbench, making it faster. See /docs or /redocs for endpoints."}

# test i/o bound tasks
@app.get("/is-io-async-good")
async def io_async_good():
    """
        # Performs multiple I/O tasks concurrently using
        # asyncio.gather.
    """
    start_time = time.time()

    tasks = {
        save_to_file_async("test11.txt"),
        save_to_file_async("test21.txt"),
        save_to_file_async("test12.txt"),
        save_to_file_async("test22.txt"),
        save_to_file_async("test13.txt"),
        save_to_file_async("test23.txt"),
        save_to_file_async("test14.txt"),
        save_to_file_async("test24.txt"),
    }
    results = await asyncio.gather(*tasks)
    end_time = time.time()

    return {
        "task": "Concurrent I/O (correct)",
        "duration_seconds": f"{end_time - start_time:.2f}",
        "results": results,
        "comment": "Total time should be approx a second, not 2, as i/o ran in parallel"
    }