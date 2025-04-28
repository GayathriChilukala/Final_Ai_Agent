# 🏠 Pic2Plot - Smart Floor Plan & Room Analyzer

## Overview

Pic2Plot is a Python application that uses AI to generate floor plans, real estate descriptions, and health recommendations from room photos or text descriptions. It's built using Chainlit for the user interface, MCP for handling AI tasks, and various libraries for image processing and AI model interaction.

## Features

-   **Images to Floor Plan**: Upload room images to automatically create a detailed floor plan.
-   **Text to Floor Plan**: Provide a text description of a space, and the AI will turn it into a floor plan.
-   **Images to Real Estate Description**: Get professional real estate listing descriptions from uploaded room images.
-   **Health Recommendations from Room Images**: Receive personalized suggestions to improve your room's health, lighting, or ergonomics.

## Architecture

The application consists of three main parts:

1.  **Server (`server.py`)**:
    * Sets up an MCP server to expose AI tools.
    * Defines functions for:
        * Analyzing room layouts from text descriptions.
        * Generating floor plans from descriptions using DALL-E.
        * Finding similar floor plans from a database.
        * Generating real estate descriptions from images.
        * Analyzing room images to provide health tips.
    * Uses Azure AI services, Sentence Transformers, and custom logic for image and text processing.

2.  **Client (`client.py`)**:
    * Uses Chainlit to create an interactive chat interface.
    * Handles user input (images and text).
    * Communicates with the MCP server to process the data.
    * Displays the results to the user.

3.  **Runner (`run.py`)**:
    * Starts the Chainlit application.
    * Optionally sets up an ngrok tunnel to make the application accessible over the internet.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
    
3.  **Set up Azure credentials:**
    * You'll need an Azure account and API keys for the Azure AI services used in `server.py`.  Replace the placeholder values (e.g., `your_githubtoken`, `your_token`) in `server.py` with your actual credentials.
    * If using ngrok, replace `your_auth_token` in `run.py` with your ngrok auth token.

4.  **Run the application:**
    **Important:** Start the server first, then the client.
    ```bash
    python server.py
    python run.py
    ```
    This will start the MCP server, and then the Chainlit application.  If configured, the application will be accessible via the ngrok URL.

## Usage

1.  **Start the application:**
    * Run `python server.py` to start the MCP server.
    * Run `python run.py` to start the Chainlit application.
2.  **Interact with the Chatbot:** Open the provided URL in your browser to access the Pic2Plot chat interface.
3.  **Input:**
    * Upload room images:  The application will attempt to generate a floor plan, real estate description, and/or health tips, depending on the server-side tools that are configured.
    * Type a text description:  Describe the desired floor plan, and the application will attempt to find similar plans.
4.  **Output:** The application will display the generated floor plan, real estate description, or health tips.

# Project Tech Stack

## Core Technologies

* **Programming Language:** Python
* **Web Framework:** Chainlit (for the user interface)
* **MCP:** A custom framework (FastMCP) for defining and running tools

## Key Components & Libraries

* **Azure OpenAI:** Used for AI model interactions, specifically the Chat Completions API.
* **Models:**
    * GPT-4 (for image analysis, description, and floorplan generation)
    * Phi-3 (for processing user input and extracting floorplan information)
    * Llama 3 (for generating health tips from images)
    * DALL-E 3 (for generating floor plan images)
* **Image Processing:** PIL (Python Imaging Library)
* **Data Handling:** Pandas
* **Sentence Transformers:** For calculating embedding similarities.
* **Networking:** `requests`
* **Other:** `asyncio`, `base64`

## Infrastructure

* **Azure Machine Learning (AML):** The project is developed and run on Azure Machine Learning.
  

## Configuration

* `run.py`:  Configures the ngrok tunnel (port, auth token) and starts the Chainlit application.
* `server.py`:  Contains the server-side logic, including API keys and model endpoints for Azure AI.
* `client.py`:  Sets up the Chainlit client and defines how user input is processed and sent to the server.

## Notes

* Ensure that the server (`server.py`) is running and the necessary AI models and APIs are accessible *before* starting the client (`run.py`).
* The application assumes that the required Azure services and models are deployed and configured correctly.
* The `requirements.txt` file should contain all the necessary Python packages.
* Ngrok is used to expose the local Chainlit application to the internet.  You can modify `run.py` if you have other deployment needs.
* The application uses a function `encode_image` in server.py, but the encoded image is not actually used in the current version of client.py.


## Team Members

- **Danny Favela** — dfavela@gmail.com
- **Dongdong Li** — dongdong@outlook.co.nz
- **Gayathri Chilukala** — gchilukala2023@fau.edu
- **Tiffany Siman** — tiffanysiman@gmail.com

