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
* Limited Accuracy/Relevance
* Lack of Integration

## How This Implementation Addresses the Problem

Pic2Plot addresses these problems through:

* **Efficiency**:
    * FastMCP framework for optimized communication.
    * `asyncio` for concurrent operations.
* **Cost Optimization & Adaptive LLM Usage**: Strategic selection of Azure OpenAI models based on use-case complexity.
* **Accuracy and Relevance**:
    * GPT-4 for image and text analysis.
    * Detailed prompt engineering for accurate room descriptions.
    * Semantic similarity search for relevant floor plan retrieval.
* **Modularity and Integration**: Chainlit for a user-friendly chat interface.
* **Unique Feature**: Health recommendations from room images.


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

