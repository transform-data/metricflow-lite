import pytest

from metricflow_lite.model.model_validator import ModelValidator
from metricflow_lite.model.objects.data_source import Mutability, MutabilityType
from metricflow_lite.model.objects.elements.dimension import Dimension, DimensionType, DimensionTypeParams
from metricflow_lite.model.objects.elements.measure import Measure, AggregationType
from metricflow_lite.model.objects.metric import MetricType, MetricTypeParams
from metricflow_lite.model.objects.user_configured_model import UserConfiguredModel
from metricflow_lite.model.validations.validator_helpers import ModelValidationException
from metricflow_lite.test.model.validations.helpers import data_source_with_guaranteed_meta, metric_with_guaranteed_meta
from metricflow_lite.time.time_granularity import TimeGranularity


@pytest.mark.skip("TODO: Will convert to validation rule")
def test_inconsistent_elements() -> None:  # noqa:D
    dim_name = "ename"
    measure_name = "ename"
    with pytest.raises(ModelValidationException):
        ModelValidator().checked_validations(
            UserConfiguredModel(
                data_sources=[
                    data_source_with_guaranteed_meta(
                        name="s1",
                        sql_query="SELECT foo FROM bar",
                        dimensions=[
                            Dimension(
                                name=dim_name,
                                type=DimensionType.TIME,
                                type_params=DimensionTypeParams(
                                    time_granularity=TimeGranularity.DAY,
                                ),
                            )
                        ],
                        mutability=Mutability(type=MutabilityType.IMMUTABLE),
                    ),
                    data_source_with_guaranteed_meta(
                        name="s2",
                        sql_query="SELECT foo FROM bar",
                        measures=[Measure(name=measure_name, agg=AggregationType.SUM)],
                        mutability=Mutability(type=MutabilityType.IMMUTABLE),
                    ),
                ],
                metrics=[
                    metric_with_guaranteed_meta(
                        name=measure_name,
                        type=MetricType.MEASURE_PROXY,
                        type_params=MetricTypeParams(measures=[measure_name]),
                    )
                ],
                materializations=[],
            )
        )
