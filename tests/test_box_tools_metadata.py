from datetime import datetime
from typing import Any, Dict

import pytest
from box_ai_agents_toolkit.box_api_metadata_template import (
    _box_metadata_template_create,
    _box_metadata_template_delete,
)

from box_tools_generic import get_box_client
from box_tools_metadata import (
    box_metadata_delete_instance_on_file_tool,
    box_metadata_get_instance_on_file_tool,
    box_metadata_set_instance_on_file_tool,
    box_metadata_template_get_by_key_tool,
    box_metadata_template_get_by_name_tool,
)


def get_metadata() -> Dict[str, Any]:
    """Generate a sample metadata instance for testing."""
    date = datetime(2023, 10, 1)
    formatted_datetime = date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return {
        "test_field": "Test Value",
        "date_field": formatted_datetime,
        "float_field": 3.14,
        "enum_field": "option1",
        "multiselect_field": ["option1", "option2"],
    }


@pytest.fixture
def template_name():
    """Generate a unique template name for testing."""
    return f"Pytest Template {datetime.now().isoformat()}"


@pytest.fixture
def created_template(ctx, template_name: str):
    """Create a metadata template for testing and clean up afterward."""
    fields = []

    field_text = {
        "type": "string",
        "displayName": "Test Field",
        "key": "test_field",
    }
    fields.append(field_text)

    field_date = {
        "type": "date",
        "displayName": "Date Field",
        "key": "date_field",
    }
    fields.append(field_date)

    field_float = {
        "type": "float",
        "displayName": "Float Field",
        "key": "float_field",
    }
    fields.append(field_float)

    field_enum = {
        "type": "enum",
        "displayName": "Enum Field",
        "key": "enum_field",
        "options": [
            {"key": "option1"},
            {"key": "option2"},
        ],
    }
    fields.append(field_enum)

    field_multiselect = {
        "type": "multiSelect",
        "displayName": "Multiselect Field",
        "key": "multiselect_field",
        "options": [
            {"key": "option1"},
            {"key": "option2"},
        ],
    }
    fields.append(field_multiselect)

    box_client_ccg = get_box_client(ctx)

    template = _box_metadata_template_create(
        box_client_ccg, display_name=template_name, fields=fields
    )

    yield template
    # Cleanup
    try:
        _box_metadata_template_delete(
            box_client_ccg, template_key=template.template_key
        )
    except Exception:
        pass  # Template might already be deleted


@pytest.mark.asyncio
async def test_box_metadata_template_get_by_key_tool(ctx, created_template):
    resp = await box_metadata_template_get_by_key_tool(
        ctx, created_template.template_key
    )
    assert resp is not None
    assert isinstance(resp, dict)
    assert resp.get("templateKey") == created_template.template_key

    # Test non-existent template
    non_existent_key = "non_existent_template_key"
    resp = await box_metadata_template_get_by_key_tool(ctx, non_existent_key)
    assert resp is not None
    assert isinstance(resp, dict)
    # The response should contain 404
    assert "error" in resp
    assert "404" in resp["error"]


@pytest.mark.asyncio
async def test_box_metadata_template_get_by_name_tool(ctx, created_template):
    resp = await box_metadata_template_get_by_name_tool(
        ctx, created_template.display_name
    )
    assert resp is not None
    assert isinstance(resp, dict)
    assert resp.get("displayName") == created_template.display_name

    # Test non-existent template
    non_existent_name = "Non Existent Template"
    resp = await box_metadata_template_get_by_name_tool(ctx, non_existent_name)
    assert resp is not None
    assert isinstance(resp, dict)
    assert "message" in resp
    assert "Template not found" in resp["message"]

    # Test with mixed case
    resp = await box_metadata_template_get_by_name_tool(
        ctx, created_template.display_name.lower()
    )
    assert resp is not None
    assert isinstance(resp, dict)
    assert resp.get("displayName") == created_template.display_name


@pytest.mark.asyncio
async def test_box_metadata_set_get_instance_on_file_tool(ctx, created_template):
    """Test setting a metadata template instance on a file."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    metadata = get_metadata()

    resp = await box_metadata_set_instance_on_file_tool(
        ctx, created_template.template_key, file_id, metadata
    )
    assert resp is not None
    assert isinstance(resp, dict)
    assert resp["$parent"] == f"file_{file_id}"
    assert resp["$template"] == created_template.template_key
    extra_data = resp.get("extra_data", {})
    assert extra_data.get("test_field") == metadata["test_field"]
    assert extra_data.get("date_field") == metadata["date_field"]
    assert extra_data.get("float_field") == metadata["float_field"]
    assert extra_data.get("enum_field") == metadata["enum_field"]
    assert extra_data.get("multiselect_field") == metadata["multiselect_field"]

    response_get = await box_metadata_get_instance_on_file_tool(
        ctx, file_id=file_id, template_key=created_template.template_key
    )
    assert response_get is not None
    assert isinstance(response_get, dict)
    assert response_get["$parent"] == f"file_{file_id}"
    assert response_get["$template"] == created_template.template_key
    extra_data_get = response_get.get("extra_data", {})
    assert extra_data_get.get("test_field") == metadata["test_field"]
    assert extra_data_get.get("date_field") == metadata["date_field"]
    assert extra_data_get.get("float_field") == metadata["float_field"]
    assert extra_data_get.get("enum_field") == metadata["enum_field"]
    assert extra_data_get.get("multiselect_field") == metadata["multiselect_field"]


@pytest.mark.asyncio
async def test_box_metadata_delete_instance_on_file_tool(ctx, created_template):
    """Test deleting a metadata template instance on a file."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    metadata = get_metadata()
    # Set metadata on the file
    response = await box_metadata_set_instance_on_file_tool(
        ctx, created_template.template_key, file_id, metadata
    )
    assert response is not None

    # Now delete the metadata instance
    response_delete = await box_metadata_delete_instance_on_file_tool(
        ctx, file_id=file_id, template_key=created_template.template_key
    )
    assert response_delete is not None  # Assuming delete returns None on success
    assert isinstance(response_delete, dict)
    assert response_delete.get("message") == "Metadata instance deleted successfully"

    # Verify that the metadata instance is deleted
    response_get = await box_metadata_get_instance_on_file_tool(
        ctx, file_id=file_id, template_key=created_template.template_key
    )
    assert response_get is not None
    assert isinstance(response_get, dict)
    assert response_get.get("error") is not None
    # Error contains a 404
    assert "404" in response_get["error"]
