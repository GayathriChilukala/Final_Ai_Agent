import asyncio
import base64
import io
import json
import requests
from collections import deque
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

# Your SAS URL for storing history
sas_url = "YOUR_SAS_URL_HERE"

async def encode_chainlit_file_to_base64(file: cl.File) -> str:
    """Asynchronously read and encode a Chainlit file to base64."""
    content = await file.read()
    return base64.b64encode(content).decode("utf-8")

async def update_history(usecase: str, result):
    """Updates the history JSON file in Azure Blob Storage, handling different result types."""
    new_record = {"usecase": usecase, "result": result}
    try:
        # Fetch existing history
        response = requests.get(sas_url)
        response.raise_for_status()

        try:
            existing_data = response.json()
            if not isinstance(existing_data, list):
                print("Existing JSON is not a list. Fixing...")
                existing_data = [existing_data]
        except json.JSONDecodeError:
            print("JSON is empty or invalid. Starting fresh...")
            existing_data = []

        # Use deque to automatically manage size
        history = deque(existing_data, maxlen=10)
        history.appendleft(new_record)  # Add the new record at the beginning

        updated_json_data = json.dumps(list(history), indent=4)

        # Upload the updated history
        headers = {"x-ms-blob-type": "BlockBlob", "Content-Type": "application/json"}
        upload_response = requests.put(sas_url, headers=headers, data=updated_json_data)
        upload_response.raise_for_status()

        print("Updated JSON successfully uploaded!")

    except requests.exceptions.RequestException as e:
        print(f"Error updating history: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding existing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



@cl.on_chat_start
async def on_chat_start():
    # Welcome message
    await cl.Message(
        content="""

# 🏠 Pic2Plot - Smart Floor Plan & Room Analyzer

Welcome! Upload room photos or provide a text description — I'll generate floor plans, real estate descriptions, or even health tips based on your rooms!

## What you can do:
- 🖼️ **Images to Floor Plan**: Upload room images to automatically create a detailed floor plan.
- ✍️ **Text to Floor Plan**: Provide a text description of a space, and I'll turn it into a floor plan.
- 🏡 **Images to Real Estate Description**: Get professional real estate listing descriptions from your uploaded room images.
- 💡 **Health Recommendations from Room Images**: Receive personalized suggestions to improve your room's health, lighting, or ergonomics.

## How to use:
1. Upload room images **or** type a description.
2. Wait a moment while the AI processes your input.
3. Get your generated floor plan, description, or health tips!

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
        await cl.Message(content="Loading...⏳").send()
        if action == "generate_health_tips_from_image":
            tool = next(tool for tool in global_tools if tool.name == "generate_health_tips_from_image")
            result = await tool.ainvoke({"image_paths": encoded_images})
            await cl.Message(content=result).send()
            await update_history("generate_health_tips_from_image", result)

        elif action == "generate_real_estate_description_from_images":
            tool = next(tool for tool in global_tools if tool.name == "generate_real_estate_description_from_images")
            result = await tool.ainvoke({"image_paths": encoded_images})
            await cl.Message(content=result).send()
            await update_history("generate_real_estate_description_from_images", result)

        elif action == "analyze_images_and_generate_floorplan":
            tool = next(tool for tool in global_tools if tool.name == "analyze_images_and_generate_floorplan")
            floorplan_image = await tool.ainvoke({"image_paths": encoded_images})
            await cl.Message(
                content=f"🛠️ Generated floorplan based on your request: '{user_text}'",
                elements=[cl.Image(name="Floorplan", display="inline", url=floorplan_image)]
            ).send()
            await update_history("analyze_images_and_generate_floorplan", floorplan_image)

        else:
            tool = next(tool for tool in global_tools if tool.name == "process_query")
            image_urls = await tool.ainvoke({"user_query": user_text})
            elements = [cl.Image(url=url, display="inline") for url in image_urls]
            await cl.Message(
                content="📋 Here are some floor plans based on your description!",
                elements=elements
            ).send()
            await update_history("text_to_floorplan", image_urls)  # Pass the list of URLs directly

    except Exception as e:
        print(f"Error: {e}")
        await cl.Message(content="❗ Sorry, something went wrong processing your request.").send()
