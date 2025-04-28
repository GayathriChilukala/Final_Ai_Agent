# 🏠 Pic2Plot - Smart Floor Plan & Room Analyzer

Welcome to **Pic2Plot** — a powerful tool that turns room images or text descriptions into smart floor plans, real estate listings, or health tips for better living!

## ✨ Features

- 🖼️ **Images to Floor Plan**  
  Upload room images and automatically create detailed floor plans using AI.

- ✍️ **Text to Floor Plan**  
  Describe your space, and Pic2Plot will generate a realistic floor plan sketch.

- 🏡 **Images to Real Estate Description**  
  Get professional real estate listing descriptions directly from your room photos.

- 💡 **Health Recommendations from Room Images**  
  Receive personalized suggestions for improving lighting, ventilation, ergonomics, and overall room wellness.

---

## 📂 Project Structure

| File         | Purpose |
|--------------|---------|
| `server.py`  | Defines all the AI tools (floorplan generation, real estate description, health tips) using MCP server. |
| `client.py`  | Handles Chainlit user interaction (uploading images or text, selecting the right tool). |
| `run.py`     | Starts the Chainlit app and exposes it publicly using Ngrok for easy sharing. |

---


## 🚀 How to Run

1. **Install Requirements**  
   ```bash
   pip install -r requirements.txt
