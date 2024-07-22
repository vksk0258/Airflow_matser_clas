from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
import pendulum

with DAG(
        dag_id='dags_simple_http_operator',
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        catchup=False,
        schedule=None,
        tags=["인프런",'python','api','공공데이터']
) as dag:
    '''실시간 지하철 위치 정보'''
    realtime_position_info = SimpleHttpOperator(
        task_id='tb_cycle_station_info',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/json/realtimePosition/0/1/1호선',
        method='GET',
        headers={'Content-Type': 'application/json',
                 'charset': 'utf-8',
                 'Accept': '*/*'
                 }
    )


    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        rslt = ti.xcom_pull(task_ids='realtime_position_info')
        import json
        from pprint import pprint

        pprint(json.loads(rslt))


    realtime_position_info >> python_2()