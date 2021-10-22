from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable
from airflow.version import version
from datetime import datetime, timedelta

default_args = {
    'owner': 'Safira_bigdata',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG('get_inflacao_python_conteiner',
         start_date=datetime(2018, 1, 1),
         max_active_runs=16,
         schedule_interval= "4 20 * * *",  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         catchup=False # enable if you don't want historical dag runs to run
         ) as dag:

        get_inflacao_python_conteiner= KubernetesPodOperator(
            task_id="get_inflacao_python_conteiner1",
            namespace="airflow",
            image="igormagro/python_container:latest",
            arguments=["/opt/app/get_inflacao.py"],
            image_pull_policy="Always",
            name="get_inflacao",
            is_delete_operator_pod=True,
            in_cluster=True,
            get_logs=True
        ) 


get_inflacao_python_conteiner