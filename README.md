# Gemini CLI Server & Obsidian Vault Integration

## Overview
This project provides a command-line interface (CLI) to interact with a local AI model (such as LM Studio) and your Obsidian note vault. It enables private, offline AI-powered search and Q&A over your personal notes and other data sources.

## Features
- **Chat with Local AI**: Use the CLI to ask questions and get answers from a local language model.
- **Obsidian Vault Search**: Query your Obsidian notes directly from the CLI using special commands.
- **Tool Integration**: Easily extendable to connect with other tools or data sources via the MCP server.
- **Privacy First**: All processing happens locally; your data never leaves your machine.

## How It Works
- The `gemini-cli-server.py` script is the main entry point. It loads configuration from `settings.json` and connects to your local AI model and the MCP server.
- Special commands (like `@obsidian`) let you search your Obsidian vault. The CLI sends these queries to the MCP server, which fetches relevant notes and returns them to the CLI.
- The AI model uses the context from your notes to answer your questions.

## Getting Started
1. **Install Requirements**
   - Python 3.8+
   - `requests` library (`pip install requests`)
   - (Optional) [LM Studio](https://lmstudio.ai/) or another OpenAI-compatible local model server

2. **Prepare Configuration**
   - Copy or create a `settings.json` file with your model and MCP server details.
   - Example:
     ```json
     {
       "model_provider": {
         "base_url": "http://localhost:1234/v1",
         "model": "your-model-name"
       },
       "mcp_servers": {
         "obsidian": {
           "endpoint": "http://localhost:8080"
         }
       }
     }
     ```

3. **Run the CLI**
   ```sh
   python gemini-cli-server.py
   ```

4. **Usage**
   - Type your questions directly.
   - Use `@obsidian <your search>` to search your Obsidian vault.
   - Type `exit` to quit.

## File Structure
- `gemini-cli-server.py` — Main CLI script
- `settings.json` — Configuration for model and MCP server
- `obsidianVault/` — Your Obsidian notes (ignored by git)
- `tmp/` — Temporary files (ignored by git)
- `.gitignore` — Excludes sensitive and unnecessary files from version control

## Notes
- Make sure your LM Studio server and MCP server are running before starting the CLI.
- The project is designed for privacy and local-first workflows.

## License
MIT License
