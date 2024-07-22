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
    '''서울시 위생업소 전체 행정처분내역 현황'''
    SeoulAdminMesure_info = SimpleHttpOperator(
        task_id='tb_cycle_station_info',
        http_conn_id='openapi.seoul.go.kr',
        endpoint='{{var.value.apikey_openapi_seoul_go_kr}}/json/SeoulAdminMesure/1/5',
        method='GET',
        headers={'Content-Type': 'application/json',
                 'charset': 'utf-8',
                 'Accept': '*/*'
                 }
    )


    @task(task_id='python_2')
    def python_2(**kwargs):
        ti = kwargs['ti']
        rslt = ti.xcom_pull(task_ids='SeoulAdminMesure_info')
        import json
        from pprint import pprint

        pprint(json.dumps(rslt))


    SeoulAdminMesure_info >> python_2()