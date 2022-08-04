from metricflow_lite.protocols.sql_client import SqlClient
from metricflow_lite.dataflow.sql_table import SqlTable
from metricflow_lite.execution.execution_plan import (
    ExecutionPlan,
    SelectSqlQueryToDataFrameTask,
    SelectSqlQueryToTableTask,
)
from metricflow_lite.execution.executor import SequentialPlanExecutor
from metricflow_lite.object_utils import random_id
from metricflow_lite.sql.sql_bind_parameters import SqlBindParameters
from metricflow_lite.sql_clients.sql_utils import make_df
from metricflow_lite.test.compare_df import assert_dataframes_equal
from metricflow_lite.test.fixtures.setup_fixtures import MetricFlowTestSessionState


def test_read_sql_task(sql_client: SqlClient) -> None:  # noqa: D
    task = SelectSqlQueryToDataFrameTask(sql_client, "SELECT 1 AS foo", SqlBindParameters())
    execution_plan = ExecutionPlan("plan0", leaf_tasks=[task])

    results = SequentialPlanExecutor().execute_plan(execution_plan)
    task_result = results.get_result(task.task_id)

    assert not results.contains_task_errors
    assert task_result.df is not None

    assert_dataframes_equal(
        actual=task_result.df,
        expected=make_df(
            sql_client=sql_client,
            columns=["foo"],
            data=[(1,)],
        ),
    )


def test_write_table_task(mf_test_session_state: MetricFlowTestSessionState, sql_client: SqlClient) -> None:  # noqa: D
    output_table = SqlTable(schema_name=mf_test_session_state.mf_system_schema, table_name=f"test_table_{random_id()}")
    task = SelectSqlQueryToTableTask(
        sql_client=sql_client,
        sql_query="SELECT 1 AS foo",
        execution_parameters=SqlBindParameters(),
        output_table=output_table,
    )
    execution_plan = ExecutionPlan("plan0", leaf_tasks=[task])

    results = SequentialPlanExecutor().execute_plan(execution_plan)

    assert not results.contains_task_errors
    assert sql_client.table_exists(output_table)

    assert_dataframes_equal(
        actual=sql_client.query(f"SELECT * FROM {output_table.sql}"),
        expected=make_df(
            sql_client=sql_client,
            columns=["foo"],
            data=[(1,)],
        ),
    )
    sql_client.drop_table(output_table)
