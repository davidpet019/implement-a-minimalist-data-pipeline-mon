from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from typing import List
import time

app = FastAPI()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PipelineRun(BaseModel):
    pipeline_name: str
    start_time: int
    end_time: int
    status: str

class PipelineMetric(BaseModel):
    pipeline_name: str
    metric_name: str
    value: float
    timestamp: int

pipelines_runs = []
pipelines_metrics = []

@app.post("/pipeline_run")
async def create_pipeline_run(pipeline_run: PipelineRun):
    pipelines_runs.append(pipeline_run)
    logger.info(f"Created pipeline run for {pipeline_run.pipeline_name}")
    return pipeline_run

@app.post("/pipeline_metric")
async def create_pipeline_metric(pipeline_metric: PipelineMetric):
    pipelines_metrics.append(pipeline_metric)
    logger.info(f"Created metric for {pipeline_metric.pipeline_name}")
    return pipeline_metric

@app.get("/pipeline_runs", response_model=List[PipelineRun])
async def get_pipeline_runs():
    return pipelines_runs

@app.get("/pipeline_metrics", response_model=List[PipelineMetric])
async def get_pipeline_metrics():
    return pipelines_metrics

@app.get("/pipeline_runs/{pipeline_name}", response_model=List[PipelineRun])
async def get_pipeline_runs_by_name(pipeline_name: str):
    return [run for run in pipelines_runs if run.pipeline_name == pipeline_name]

@app.get("/pipeline_metrics/{pipeline_name}", response_model=List[PipelineMetric])
async def get_pipeline_metrics_by_name(pipeline_name: str):
    return [metric for metric in pipelines_metrics if metric.pipeline_name == pipeline_name]