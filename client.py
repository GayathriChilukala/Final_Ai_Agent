import asyncio
import base64
import io

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from PIL import Image
import chainlit as cl

# Global tools variable
global_tools = []

# Server parameters
server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)

async def encode_chainlit_file_to_base64(file: cl.File) -> str:
    """Asynchronously read and encode a Chainlit file to base64."""
    content = await file.read()
    return base64.b64encode(content).decode("utf-8")


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="""
# 🏠 Pic2Plot - Smart Floor Plan & Room Analyzer

Welcome! Upload room photos or provide a text description — I'll generate floor plans, real estate descriptions, or even health tips based on your rooms!

## What you can do:
- 🖼️ **Images to Floor Plan**
- ✍️ **Text to Floor Plan**
- 🏡 **Images to Real Estate Description**
- 💡 **Health Recommendations from Room Images**

Let's get started!
"""
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages."""
    global global_tools

    user_text = message.content.strip() if message.content else ""
    image_files = [file for file in message.elements if "image" in file.mime] if message.elements else []

    # Encode images if any
    encoded_images = []
    if image_files:
        for img in image_files:
            encoded = await encode_chainlit_file_to_base64(img)
            encoded_images.append({
                "data": encoded,
                "mime": img.mime
            })

    # Initialize tools if not already done
    if not global_tools:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                global_tools = await load_mcp_tools(session)
                print(f"✅ Loaded Tools: {[tool.name for tool in global_tools]}")

    if not global_tools:
        await cl.Message(content="❌ Error: Tools could not be loaded.").send()
        return

    # Choose the tool based on user input
    user_func = next((tool for tool in global_tools if tool.name == "get_function_name_from_user_input"), None)

    if not user_func:
        await cl.Message(content="❌ Error: Tool 'get_function_name_from_user_input' not found.").send()
        return

    try:
        action = await user_func.ainvoke({"user_input": user_text})

        if action == "generate_health_tips_from_image":
            tool = next(tool for tool in global_tools if tool.name == "generate_health_tips_from_image")
            result = await tool.ainvoke({"image_paths": encoded_images})
            await cl.Message(content=result).send()

        elif action == "generate_real_estate_description_from_images":
            tool = next(tool for tool in global_tools if tool.name == "generate_real_estate_description_from_images")
            result = await tool.ainvoke({"image_paths": encoded_images})
            await cl.Message(content=result).send()

        elif action == "analyze_images_and_generate_floorplan":
            tool = next(tool for tool in global_tools if tool.name == "analyze_images_and_generate_floorplan")
            floorplan_image = await tool.ainvoke({"image_paths": encoded_images})
            await cl.Message(
                content=f"🛠️ Generated floorplan based on your request: '{user_text}'",
                elements=[cl.Image(name="Floorplan", display="inline", url=floorplan_image)]
            ).send()

        else:
            tool = next(tool for tool in global_tools if tool.name == "process_query")
            image_urls = await tool.ainvoke({"user_query": user_text})
            elements = [cl.Image(url=url, display="inline") for url in image_urls]
            await cl.Message(
                content="📋 Here are some floor plans based on your description!",
                elements=elements
            ).send()

    except Exception as e:
        print(f"Error: {e}")
        await cl.Message(content="❗ Sorry, something went wrong processing your request.").send()
