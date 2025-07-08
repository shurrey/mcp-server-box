from datetime import datetime
from typing import List

import pytest
from box_ai_agents_toolkit.box_api_metadata_template import (
    BoxClient,
    _box_metadata_template_create,
    _box_metadata_template_delete,
)

from box_tools_generic import get_box_client
from box_tools_metadata import (
    box_metadata_template_get_by_key_tool,
    box_metadata_template_get_by_name_tool,
)


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
    # The response should contain 404
    assert "message" in resp
    assert "Template not found" in resp["message"]
