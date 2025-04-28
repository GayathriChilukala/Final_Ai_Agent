# 🏠 Pic2Plot - Smart Floor Plan & Room Analyzer

## Overview

Pic2Plot is a Python application that uses AI to generate floor plans, real estate descriptions, and health recommendations from room photos or text descriptions. It's built using Chainlit for the user interface, MCP for handling AI tasks, and various libraries for image processing and AI model interaction.

## Features

-   **Images to Floor Plan**: Upload room images to automatically create a detailed floor plan.
-   **Text to Floor Plan**: Provide a text description of a space, and the AI will turn it into a floor plan.
-   **Images to Real Estate Description**: Get professional real estate listing descriptions from uploaded room images.
-   **Health Recommendations from Room Images**: Receive personalized suggestions to improve your room's health, lighting, or ergonomics.


## Problem Statement

Current floorplan generation solutions often suffer from:

* High Latency
* High Cost

## How This Implementation Addresses the Problem

Pic2Plot addresses these problems through:

* **Efficiency**:
    * FastMCP framework for optimized communication.
    * `asyncio` for concurrent operations.
* **Cost Optimization & Adaptive LLM Usage**: Strategic selection of Azure OpenAI models based on use-case complexity.
   * Example: For simple text processing, Pic2Plot uses Phi-3, a smaller, less expensive model
* **Unique Feature**: Health recommendations from room images.


## Architecture

[View Diagram](path/to/your/Untitled%20Diagram.drawio%20(1).html)

<img src="data:image/jpeg;base64,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" alt="Alt text">

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
    

## Project Tech Stack

### Core Technologies

* **Programming Language:** Python
* **Web Framework:** Chainlit (for the user interface)
* **MCP:** A custom framework (FastMCP) for defining and running tools
  

### Key Components & Libraries

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


### Infrastructure

* **Azure Machine Learning (AML):** The project is developed and run on Azure Machine Learning.
  

## Configuration

* `run.py`:  Configures the ngrok tunnel (port, auth token) and starts the Chainlit application.
* `server.py`:  Contains the server-side logic, including API keys and model endpoints for Azure AI.
* `client.py`:  Sets up the Chainlit client and defines how user input is processed and sent to the server.



## Team Members

- **Danny Favela** — dfavela@gmail.com
- **Dongdong Li** — dongdong@outlook.co.nz
- **Gayathri Chilukala** — gchilukala2023@fau.edu
- **Tiffany Siman** — tiffanysiman@gmail.com

