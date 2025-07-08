from box_ai_agents_toolkit import (
    box_metadata_template_get_by_key,
    box_metadata_template_get_by_name,
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
