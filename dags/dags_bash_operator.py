from airflow import DAG
import datetime
import pendulum

from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dags_bash_operator",
    # 이덱은 매일 0시 0분에 시작
    schedule="0 0 * * *",
    # 덱이 언제 부터 돌지 TZ=타임존
    start_date=pendulum.datetime(2021, 1, 1, tz="Asia/Seoul"),
    # 캐치업 배치 중간에 누락된 구간을 돌릴지 말지
    # 1월 1일부터 3월 1일까지 누락된 덱을 한번에 돌아가게 된다 3월 1일에 웬만하면 false
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["인프런","bash"]
    ) as dag:
    run_this = BashOperator(
        # 객체명과 task id 는 같게 가는게 좋다

        task_id="run_this",
        bash_command="echo whoami",
    )

    run_echo_hostname = BashOperator(
        # 객체명과 task id 는 같게 가는게 좋다
        task_id="echo_hostname",
        bash_command="echo $HOSTNAME",
    )

    run_this >> run_echo_hostname