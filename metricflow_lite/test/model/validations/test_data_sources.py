import pytest

from metricflow_lite.model.objects.data_source import MutabilityType, Mutability
from metricflow_lite.model.objects.elements.dimension import Dimension, DimensionType, DimensionTypeParams
from metricflow_lite.model.validations.validator_helpers import ModelValidationException
from metricflow_lite.test.model.validations.helpers import data_source_with_guaranteed_meta
from metricflow_lite.time.time_granularity import TimeGranularity


@pytest.mark.skip("TODO: Will convert to validation rule")
def test_data_source_invalid_sql() -> None:  # noqa:D
    with pytest.raises(ModelValidationException, match=r"Invalid SQL"):
        data_source_with_guaranteed_meta(
            name="invalid_sql_source",
            sql_query="SELECT foo FROM bar;",
            dimensions=[
                Dimension(
                    name="ds",
                    type=DimensionType.TIME,
                    type_params=DimensionTypeParams(
                        time_granularity=TimeGranularity.DAY,
                    ),
                )
            ],
            mutability=Mutability(type=MutabilityType.IMMUTABLE),
        )
