import asyncio

import pytest

from tartiflette import Resolver, create_engine


@pytest.mark.asyncio
async def test_hex_color_code_ok():
    @Resolver("Query.hexColorCode", schema_name="test_hex_color_code_ok")
    async def hex_color_code_resolver(*_args, **_kwargs):
        return "#ffffff"

    sdl = """
    type Query {
        hexColorCode: HexColorCode
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hex_color_code_ok",
    )

    assert await engine.execute("query hexColorCodeOk { hexColorCode }") == {
        "data": {"hexColorCode": "#ffffff"}
    }


@pytest.mark.asyncio
async def test_hex_color_code_nok():
    @Resolver("Query.hexColorCode", schema_name="test_hex_color_code_nok")
    async def hex_color_code_resolver(*_args, **_kwargs):
        return "nope"

    sdl = """
    type Query {
        hexColorCode: HexColorCode
    }
    """

    engine = await create_engine(
        sdl=sdl,
        modules=[{"name": "tartiflette_plugin_scalars", "config": {}}],
        schema_name="test_hex_color_code_nok",
    )

    result = await engine.execute("query hexColorCodeNok { hexColorCode }")
    assert result["data"]["hexColorCode"] is None
    assert len(result["errors"]) == 1
    assert (
        result["errors"][0]["message"]
        == "Value is not a valid HexColorCode: < nope >"
    )
