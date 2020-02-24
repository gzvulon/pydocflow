import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def greet():
    print('Writing in file')
    with open('/tmp/greet.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        f.write(str(t) + '\n')
    return 'Greeted'


def respond():
    return 'Greet Responded Again'


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
    'concurrency': 1,
    'retries': 1
}

dag = DAG('my_simple_dag',
         catchup=False,
         default_args=default_args,
         # schedule_interval='*/10 * * * *',
         # schedule_interval=None,
         )
opr_hello = BashOperator(task_id='say_Hi',
                         bash_command='echo "Hi!!"',
                         dag=dag)

opr_greet = PythonOperator(task_id='greet',
                           python_callable=greet,
                           dag=dag)

# opr_sleep = BashOperator(task_id='sleep_me',
#                          bash_command='sleep 0.1')

opr_respond = PythonOperator(task_id='respond',
                             python_callable=respond,
                             dag=dag)

opr_hello >> opr_greet >> opr_respond
