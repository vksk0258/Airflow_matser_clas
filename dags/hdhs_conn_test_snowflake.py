from airflow import DAG
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator

def isrt_data():
    snowflake_hook = SnowflakeHook(snowflake_conn_id='snow_itsmart_copy1')
    conn = snowflake_hook.get_conn()
    cursor = conn.cursor()
    print(cursor)
    cursor.close()
    conn.close()

with DAG(
    dag_id='hdhs_conn_tset_snowflake',
    schedule_interval=None
) as dag:

    hdhs_task = PythonOperator(
        task_id='hdhs_task',
        python_callable=isrt_data,
    )
    hdhs_task