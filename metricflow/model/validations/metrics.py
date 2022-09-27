import traceback
from typing import List

from metricflow.errors.errors import ParsingException
from metricflow.instances import MetricModelReference
from metricflow.model.objects.metric import Metric, MetricType, CumulativeMetricWindow
from metricflow.model.objects.user_configured_model import UserConfiguredModel
from metricflow.model.validations.validator_helpers import (
    FileContext,
    MetricContext,
    ModelValidationRule,
    ValidationIssueType,
    ValidationError,
    validate_safely,
)


class CumulativeMetricRule(ModelValidationRule):
    """Checks that cumulative sum metrics are configured properly"""

    @staticmethod
    @validate_safely(whats_being_done="checking that the params of metric are valid if it is a cumulative sum metric")
    def _validate_cumulative_sum_metric_params(metric: Metric) -> List[ValidationIssueType]:
        issues: List[ValidationIssueType] = []

        if metric.type == MetricType.CUMULATIVE:
            if metric.type_params.window and metric.type_params.grain_to_date:
                issues.append(
                    ValidationError(
                        context=MetricContext(
                            file_context=FileContext.from_metadata(metadata=metric.metadata),
                            metric=MetricModelReference(metric_name=metric.name),
                        ),
                        message="Both window and grain_to_date set for cumulative metric. Please set one or the other",
                    )
                )

            if metric.type_params.window:
                try:
                    _, _ = CumulativeMetricWindow.parse(metric.type_params.window.to_string())
                except ParsingException as e:
                    issues.append(
                        ValidationError(
                            context=MetricContext(
                                file_context=FileContext.from_metadata(metadata=metric.metadata),
                                metric=MetricModelReference(metric_name=metric.name),
                            ),
                            message="".join(traceback.format_exception_only(etype=type(e), value=e)),
                            extra_detail="".join(traceback.format_tb(e.__traceback__)),
                        )
                    )

        return issues

    @staticmethod
    @validate_safely(whats_being_done="running model validation ensuring cumulative sum metrics are valid")
    def validate_model(model: UserConfiguredModel) -> List[ValidationIssueType]:  # noqa: D
        issues: List[ValidationIssueType] = []

        for metric in model.metrics or []:
            issues += CumulativeMetricRule._validate_cumulative_sum_metric_params(metric=metric)

        return issues
