from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
import pandas as pd

def snowflake_conn_test():
    snowflake_hook = SnowflakeHook(snowflake_conn_id='snow_itsmart')
    connection = snowflake_hook.get_conn()
    cursor = connection.cursor()

    result = cursor.execute("select * from PILOTDB.AIRFLOW.FINANCIAL_SC where ENTITY_NAME = 'Amalgamated Bank limit 100;")
    cursor.close()
    connection.close()
    return result

with DAG(
    dag_id="dags_snowflake_test",
    # 이덱은 매일 6시 30분에 시작
    schedule="30 6 * * *",
    # 캐치업 배치 중간에 누락된 구간을 돌릴지 말지
    # 1월 1일부터 3월 1일까지 누락된 덱을 한번에 돌아가게 된다 3월 1일에 왠만하면 false
    catchup=False,
    tags=["옵션", "태그"]
) as dag:
    extract_task = PythonOperator(
        task_id='snowflake_conn_test',
        python_callable=snowflake_conn_test
    )


    snowflake_conn_test