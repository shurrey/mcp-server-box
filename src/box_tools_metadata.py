from box_ai_agents_toolkit import (
    box_metadata_template_get_by_key,
    box_metadata_template_get_by_name,
    box_metadata_set_instance_on_file,
    box_metadata_get_instance_on_file,
)
from mcp.server.fastmcp import Context

from box_tools_generic import get_box_client


async def box_metadata_template_get_by_key_tool(
    ctx: Context, template_name: str
) -> dict:
    """
    Retrieve a metadata template by its key.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        template_key (str): The key of the metadata template to retrieve.

    Returns:
        dict: The metadata template associated with the provided key.
    """
    box_client = get_box_client(ctx)
    return box_metadata_template_get_by_key(box_client, template_name)


async def box_metadata_template_get_by_name_tool(
    ctx: Context, template_name: str
) -> dict:
    """
    Retrieve a metadata template by its name.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        template_name (str): The name of the metadata template to retrieve.

    Returns:
        dict: The metadata template associated with the provided name.
    """
    box_client = get_box_client(ctx)
    return box_metadata_template_get_by_name(box_client, template_name)


async def box_metadata_set_instance_on_file_tool(
    ctx: Context,
    template_key: str,
    file_id: str,
    metadata: dict,
) -> dict:
    """
    Set a metadata instance on a file.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        template_key (str): The key of the metadata template.
        file_id (str): The ID of the file to set the metadata on.
        metadata (dict): The metadata to set.
        Example: {'test_field': 'Test Value', 'date_field': '2023-10-01T00:00:00.000Z', 'float_field': 3.14, 'enum_field': 'option1', 'multiselect_field': ['option1', 'option2']}


    Returns:
        dict: The response from the Box API after setting the metadata.
    """
    box_client = get_box_client(ctx)
    return box_metadata_set_instance_on_file(
        box_client, template_key, file_id, metadata
    )


async def box_metadata_get_instance_on_file_tool(
    ctx: Context,
    file_id: str,
    template_key: str,
) -> dict:
    """
    Get a metadata instance on a file.

    Args:
        ctx (Context): The context object containing the request and lifespan context.
        file_id (str): The ID of the file to get the metadata from.
        template_key (str): The key of the metadata template.

    Returns:
        dict: The metadata instance associated with the file.
    """
    box_client = get_box_client(ctx)
    return box_metadata_get_instance_on_file(box_client, file_id, template_key)
