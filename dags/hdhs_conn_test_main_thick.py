from airflow import DAG
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import pandas as pd
import pprint
import time


client_path = Variable.get("client_path")
def oracle_conn_main_test():
    start = time.time()
    oracle_hook = OracleHook(oracle_conn_id='conn_oracle_main',thick_mode=True,thick_mode_lib_dir=client_path)
    sql = "SELECT * FROM HDHS_OD.OD_CRD_APRVL_LOG_CRYPT WHERE CHG_DTM BETWEEN TO_DATE('2024-11-20 13:00:00', 'YYYY-MM-DD HH24:MI:SS') AND TO_DATE('2024-11-20 14:00:00', 'YYYY-MM-DD HH24:MI:SS')"
    connection = oracle_hook.get_conn()
    cursor = connection.cursor()
    print(cursor)
    point1 = time.time()
    pprint.pprint(f"커넥션 붙는 시간: {point1 - start} sec")

    cursor.execute(sql)
    pprint.pprint("next")
    data = cursor.fetchall()
    point2 = time.time()
    pprint.pprint(f"쿼리 수행 시간: : {point2 - point1} sec")

    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    print("Number of rows:", len(df))
    cursor.close()
    connection.close()
    point3 = time.time()
    pprint.pprint(f"커넥션 끊기는데 걸리는 시간: {point3 - point2} sec")
    return

with DAG(
    dag_id="hdhs_conn_test_main_thick",
    schedule_interval=None,
    tags=["현대홈쇼핑"]
) as dag:
    var_value = Variable.get("sample_key")
    oracle_conn_test_task = PythonOperator(
        task_id='oracle_conn_test_task',
        python_callable=oracle_conn_main_test
    )

    bash_var_2 = BashOperator(
        task_id="bash_var_2",
        # 스케쥴러의 부하를 줄이기위해 템플릿 문법으로 전역변수를 가져오는 것을 추천함
        bash_command=var_value
    )

    oracle_conn_test_task >> bash_var_2