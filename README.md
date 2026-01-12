# Mocchibird Discord Chat Bot

A friendly Discord bot powered by AI that you can chat with. Mocchibird responds when mentioned (@mocchibird) and supports both local LLMs (like Ollama) and cloud APIs (like OpenAI).

## Features

- 🤖 **Discord Integration**: Responds when mentioned in any channel
- 🧠 **Multiple LLM Support**: Works with Ollama (local) or OpenAI API
- ⚙️ **Configurable**: Fine-tune personality and behavior via `config.yaml`
- 💾 **Context Memory**: Maintains conversation history per channel
- 🎓 **Training Support**: Utilities for preparing fine-tuning data
- 🔄 **Hot Reload**: Reload configuration without restarting the bot

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token ([Create one here](https://discord.com/developers/applications))
- Either:
  - Ollama installed locally ([Get Ollama](https://ollama.ai)), OR
  - OpenAI API key ([Get API key](https://platform.openai.com))

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mocchibird/mocchi-chat.git
   cd mocchi-chat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `OPENAI_API_KEY`: Your API key (or "ollama" for local Ollama)
   - `OPENAI_API_BASE`: API endpoint (default: `http://localhost:11434/v1` for Ollama)
   - `MODEL_NAME`: Model to use (e.g., `llama2`, `gpt-3.5-turbo`, `gpt-4`)

4. **Customize bot behavior (optional):**
   
   Edit `config.yaml` to customize:
   - Bot personality (system prompt)
   - Model parameters (temperature, max_tokens, etc.)
   - Context settings (conversation history length)
   - Response behavior

## Setting Up Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a New Application
3. Go to the "Bot" section and create a bot
4. Copy the bot token to your `.env` file
5. Enable "Message Content Intent" under Privileged Gateway Intents
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot`
8. Select permissions: `Send Messages`, `Read Messages/View Channels`, `Read Message History`
9. Use the generated URL to invite the bot to your server

## Setting Up Ollama (Optional - for local LLM)

1. **Install Ollama:**
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Or download from https://ollama.ai
   ```

2. **Pull a model:**
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ```

3. **Verify Ollama is running:**
   ```bash
   ollama list
   ```

## Usage

### Running the Bot

```bash
python bot.py
```

The bot will connect to Discord and start responding to mentions.

### Interacting with the Bot

Simply mention the bot in any channel:
```
@mocchibird Hello! How are you?
```

The bot will respond with an AI-generated message.

### Bot Commands

- `!clear_history` - Clear conversation history for the current channel
- `!reload_config` - Reload configuration from `config.yaml` (admin only)

## Configuration

The `config.yaml` file allows you to fine-tune the bot's behavior:

### System Prompt
Define the bot's personality and behavior:
```yaml
system_prompt: |
  You are Mocchibird, a friendly and helpful AI assistant.
  Keep responses conversational and engaging.
```

### Model Parameters
Control response generation:
```yaml
model_parameters:
  temperature: 0.7      # Creativity (0.0-2.0)
  max_tokens: 500       # Max response length
  top_p: 0.9           # Nucleus sampling
  frequency_penalty: 0.0  # Reduce repetition
  presence_penalty: 0.0   # Encourage new topics
```

### Context Settings
```yaml
context:
  max_history: 10       # Messages to remember
  use_usernames: true   # Include usernames in context
```

### Response Settings
```yaml
response:
  typing_indicator: true  # Show typing while thinking
  mention_user: true      # Reply directly to user
  error_message: "..."    # Custom error message
```

## Fine-Tuning / Training

The `training.py` script provides utilities for preparing training data.

### Create Example Training Data

```bash
python training.py
```

Select option 1 to create an example training data file.

### Prepare Training Data from Conversations

1. Create a JSON file with conversations:
   ```json
   [
     {
       "user": "Hello!",
       "assistant": "Hi! How can I help you?"
     },
     {
       "user": "What's the weather?",
       "assistant": "I don't have access to weather data, but I can help with other questions!"
     }
   ]
   ```

2. Run the training script:
   ```bash
   python training.py
   ```
   
3. Select option 2 and provide the path to your conversations file.

4. The script will generate a `.jsonl` file in the `training_data/` directory that can be used for fine-tuning with OpenAI's API.

### Update Configuration Programmatically

```bash
python training.py
```

Select option 3 to update the system prompt or model parameters.

## Using Training Data for Fine-Tuning

Once you have prepared training data, you can use it to fine-tune models:

### For OpenAI Models:

1. Upload your training file:
   ```bash
   openai api fine_tunes.create -t training_data/your_file.jsonl -m gpt-3.5-turbo
   ```

2. Wait for training to complete

3. Update your `.env` file with the fine-tuned model name

### For Local Models (Ollama):

Ollama supports creating custom models with `Modelfile`:

1. Create a `Modelfile`:
   ```
   FROM llama2
   SYSTEM "You are Mocchibird, a friendly AI assistant..."
   ```

2. Create the model:
   ```bash
   ollama create mocchibird -f Modelfile
   ```

3. Update `MODEL_NAME` in `.env` to `mocchibird`

## Project Structure

```
mocchi-chat/
├── bot.py              # Main bot implementation
├── training.py         # Training data preparation utilities
├── config.yaml         # Bot configuration and fine-tuning
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your environment variables (not in git)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Troubleshooting

### Bot doesn't respond to mentions
- Verify "Message Content Intent" is enabled in Discord Developer Portal
- Check that the bot has proper permissions in your server
- Ensure the bot is online (check console for connection message)

### API connection errors
- **Ollama**: Ensure Ollama is running (`ollama serve`)
- **OpenAI**: Verify your API key is correct
- Check the `OPENAI_API_BASE` URL is correct

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Use a virtual environment to avoid conflicts

## Development

### Running in Development Mode

For development, you might want to:
1. Enable debug logging in `bot.py`
2. Use a test Discord server
3. Use a smaller/faster model for quicker responses

### Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Uses [OpenAI API](https://platform.openai.com/docs/api-reference) (compatible with Ollama)
- Powered by [Ollama](https://ollama.ai) or OpenAI models