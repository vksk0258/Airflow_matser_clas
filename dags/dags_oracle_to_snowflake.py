from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator


with DAG(
    dag_id="dags_oracle_to_snowflake",
    # 이덱은 매일 1일 6시 30분에 시작
    schedule="30 6 1 * *",
    # 덱이 언제 부터 돌지 TZ=타임존
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    # 캐치업 배치 중간에 누락된 구간을 돌릴지 말지
    # 1월 1일부터 3월 1일까지 누락된 덱을 한번에 돌아가게 된다 3월 1일에 왠만하면 false
    catchup=False,
    tags=["옵션", "태그"]
) as dag: