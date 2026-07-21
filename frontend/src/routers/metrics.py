import logging
from pathlib import Path
from urllib.parse import urlencode
from psutil import cpu_percent, virtual_memory


from fastapi import APIRouter, Request, HTTPException

ROUTERS_DIR = Path(__file__).resolve().parent
SRC_DIR = ROUTERS_DIR.parent

router = APIRouter(
)

@router.get("/", status_code=200)
async def get_metrics(request: Request):
    """Used to check if API is running"""
    try:
        virt_mem = virtual_memory()
        cpu_utilization = cpu_percent(interval=1)
        mem_total = virt_mem.total
        mem_used = virt_mem.used
        content = f"""
vm_cpu_utilization {cpu_utilization}
vm_mem_total {mem_total}
vm_mem_used {mem_used}
"""
        return {
            "status": "healthy",
            }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))