from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable
from airflow.version import version
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG(
    'hello_world',
    start_date=datetime(2018, 1, 1),
    max_active_runs=16,
    schedule_interval= "4 20 * * *",  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    default_args=default_args,
    catchup=False, # enable if you don't want historical dag runs to run
    tags=["example"]
) as dag:

    hello_world= KubernetesPodOperator(
        task_id="hello_world",
        namespace="airflow",
        image="ibernardes/airflow-python-container:dev-latest",
        arguments=["/opt/app/exampçes/hello_world.py"],
        image_pull_policy="Always",
        name="hello_world",
        is_delete_operator_pod=True,
        in_cluster=True,
        get_logs=True
    ) 


hello_world