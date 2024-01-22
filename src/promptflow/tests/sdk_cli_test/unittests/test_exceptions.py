# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import pytest
from azure.core.exceptions import HttpResponseError
from promptflow._sdk._orm import RunInfo
from promptflow.exceptions import _ErrorInfo, ErrorCategory, ErrorTarget, UserErrorException
from promptflow.executor import FlowValidator
from promptflow.executor._errors import InvalidNodeReference

FLOWS_DIR = "./tests/test_configs/flows/print_input_flow"


@pytest.mark.unittest
class TestExceptions:
    def test_error_category_with_unknow_error(self, pf):
        ex = None
        try:
            pf.run("./exceptions/flows")
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.UNKNOWN
        assert error_type == "FileNotFoundError"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == ""
        assert (
            "module=promptflow._sdk._pf_client, "
            'code=raise FileNotFoundError(f"flow path {flow} does not exist"), '
            "lineno="
        ) in error_detail

    def test_error_category_with_user_error(self, pf):
        ex = None
        try:
            RunInfo.get("run_name")
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.USER_ERROR
        assert error_type == "RunNotFoundError"
        assert error_target == ErrorTarget.CONTROL_PLANE_SDK
        assert error_message == ""
        assert (
            "module=promptflow._sdk._orm.run_info, "
            'code=raise RunNotFoundError(f"Run name {name!r} cannot be found."), '
            "lineno="
        ) in error_detail

    def test_error_category_with_system_error(self):
        ex = None
        try:
            FlowValidator._validate_aggregation_inputs({}, {"input1": "value1"})
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.SYSTEM_ERROR
        assert error_type == "InvalidAggregationInput"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == (
            "The input for aggregation is incorrect. "
            "The value for aggregated reference input '{input_key}' should be a list, "
            "but received {value_type}. "
            "Please adjust the input value to match the expected format."
        )
        assert (
            "module=promptflow.executor.flow_validator, " "code=raise InvalidAggregationInput(, " "lineno="
        ) in error_detail

    def test_error_category_with_http_error(self, subscription_id, resource_group_name, workspace_name):
        try:
            raise HttpResponseError(message="HttpResponseError")
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.UNKNOWN
        assert error_type == "HttpResponseError"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == ""
        assert error_detail == ""

    @pytest.mark.parametrize(
        "status_code, expected_error_category",
        [
            (203, ErrorCategory.UNKNOWN),
            (304, ErrorCategory.UNKNOWN),
            (400, ErrorCategory.UNKNOWN),
            (401, ErrorCategory.UNKNOWN),
            (429, ErrorCategory.UNKNOWN),
            (500, ErrorCategory.UNKNOWN),
        ],
    )
    def test_error_category_with_status_code(self, status_code, expected_error_category):
        try:
            raise Exception()
        except Exception as e:
            e.status_code = status_code
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == expected_error_category
        assert error_type == "Exception"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == ""
        assert error_detail == ""

    def test_error_category_with_executor_error(self):
        try:
            msg_format = (
                "Invalid node definitions found in the flow graph. Non-aggregation node '{invalid_reference}' "
                "cannot be referenced in the activate config of the aggregation node '{node_name}'. Please "
                "review and rectify the node reference."
            )
            raise InvalidNodeReference(message_format=msg_format, invalid_reference=None, node_name="node_name")
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.USER_ERROR
        assert error_type == "InvalidNodeReference"
        assert error_target == ErrorTarget.EXECUTOR
        assert error_message == (
            "Invalid node definitions found in the flow graph. Non-aggregation node '{invalid_reference}' "
            "cannot be referenced in the activate config of the aggregation node '{node_name}'. Please "
            "review and rectify the node reference."
        )
        assert error_detail == ""

    def test_error_category_with_cause_exception1(self):
        """cause exception is PromptflowException and e is PromptflowException, recording e."""

        ex = None
        try:
            try:
                FlowValidator._validate_aggregation_inputs({}, {"input1": "value1"})
            except Exception as e:
                raise UserErrorException("FlowValidator._validate_aggregation_inputs failed") from e
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.USER_ERROR
        assert error_type == "InvalidAggregationInput"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == ""
        assert error_detail == ""

        ex = None
        try:
            try:
                FlowValidator._validate_aggregation_inputs({}, {"input1": "value1"})
            except Exception as e:
                raise UserErrorException(message=str(e), error=e)
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.USER_ERROR
        assert error_type == "InvalidAggregationInput"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == ""
        assert error_detail == ""

    def test_error_category_with_cause_exception2(self):
        """cause exception is PromptflowException and e is not PromptflowException, recording cause exception."""

        ex = None
        try:
            try:
                FlowValidator._validate_aggregation_inputs({}, {"input1": "value1"})
            except Exception as e:
                raise Exception("FlowValidator._validate_aggregation_inputs failed") from e
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.SYSTEM_ERROR
        assert error_type == "InvalidAggregationInput"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == (
            "The input for aggregation is incorrect. The value for aggregated reference "
            "input '{input_key}' should be a list, but received {value_type}. Please "
            "adjust the input value to match the expected format."
        )
        assert (
            "module=promptflow.executor.flow_validator, " "code=raise InvalidAggregationInput(, " "lineno="
        ) in error_detail

    def test_error_category_with_cause_exception3(self, pf):
        """cause exception is not PromptflowException and e is not PromptflowException, recording e exception."""

        ex = None
        try:
            try:
                pf.run("./exceptions/flows")
            except Exception as e:
                raise Exception("pf run failed") from e
        except Exception as e:
            ex = e
        error_category, error_type, error_target, error_message, error_detail = _ErrorInfo.get_error_info(ex)
        assert error_category == ErrorCategory.UNKNOWN
        assert error_type == "Exception"
        assert error_target == ErrorTarget.UNKNOWN
        assert error_message == ""
        assert error_detail == ""
