from typing import List

from metricflow_lite.model.objects.data_source import DataSource
from metricflow_lite.model.objects.materialization import Materialization
from metricflow_lite.model.objects.metric import Metric
from metricflow_lite.model.objects.base import HashableBaseModel


class UserConfiguredModel(HashableBaseModel):
    """Model holds all the information the SemanticLayer needs to render a query"""

    data_sources: List[DataSource]
    metrics: List[Metric]
    materializations: List[Materialization] = []
