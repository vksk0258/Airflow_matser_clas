from airflow import DAG
import datetime
import pendulum
import random
from airflow.operators.python import PythonOperator
#에어플로우는 plugins까지 패스로 받아지기때문에 이렇게 깃 푸시를 하면 에어플로우에서 에러가 난다.
from common.common_func import regist2

with DAG(
    dag_id="dags_python_with_op_kwargs",
    # 이덱은 매일 6시 30분에 시작
    schedule="30 6 * * *",
    # 덱이 언제 부터 돌지 TZ=타임존
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    # 캐치업 배치 중간에 누락된 구간을 돌릴지 말지
    # 1월 1일부터 3월 1일까지 누락된 덱을 한번에 돌아가게 된다 3월 1일에 왠만하면 false
    catchup=False,
    tags=["옵션", "태그"]
) as dag:
    regist2_t1 = PythonOperator(
        task_id='regist2_t1',
        python_callable=regist2,
        op_args=['giltaek','man','kr','crossfit'],
        op_kwarge={'email':"vksk0258@gmail.com",'phone':'5502'}
    )
    regist2_t1