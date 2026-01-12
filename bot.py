"""
Mocchibird Discord Bot - A friendly AI chat bot for Discord
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yaml
from openai import OpenAI
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('mocchibird')

# Load environment variables
load_dotenv()

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize OpenAI client (works with Ollama using OpenAI-compatible API)
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY', 'ollama'),  # Ollama doesn't need a real key
    base_url=os.getenv('OPENAI_API_BASE', 'http://localhost:11434/v1')
)

# Store conversation history per channel
conversation_history: Dict[int, List[Dict[str, str]]] = {}


def get_system_prompt() -> str:
    """Get the system prompt from config"""
    return config.get('system_prompt', 'You are a helpful AI assistant.')


def get_model_parameters() -> dict:
    """Get model parameters from config"""
    return config.get('model_parameters', {
        'temperature': 0.7,
        'max_tokens': 500,
        'top_p': 0.9,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    })


def get_conversation_context(channel_id: int) -> List[Dict[str, str]]:
    """Get conversation history for a channel"""
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []
    
    max_history = config.get('context', {}).get('max_history', 10)
    return conversation_history[channel_id][-max_history:]


def add_to_conversation(channel_id: int, role: str, content: str, username: str = None):
    """Add a message to conversation history"""
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []
    
    use_usernames = config.get('context', {}).get('use_usernames', True)
    if use_usernames and username and role == 'user':
        content = f"{username}: {content}"
    
    conversation_history[channel_id].append({
        'role': role,
        'content': content
    })


async def generate_response(prompt: str, channel_id: int, username: str = None) -> str:
    """Generate a response using the LLM"""
    try:
        # Add user message to history
        add_to_conversation(channel_id, 'user', prompt, username)
        
        # Get conversation context
        context = get_conversation_context(channel_id)
        
        # Prepare messages for API
        messages = [
            {'role': 'system', 'content': get_system_prompt()}
        ] + context
        
        # Get model parameters
        params = get_model_parameters()
        
        # Call the API
        response = client.chat.completions.create(
            model=os.getenv('MODEL_NAME', 'llama2'),
            messages=messages,
            temperature=params.get('temperature', 0.7),
            max_tokens=params.get('max_tokens', 500),
            top_p=params.get('top_p', 0.9),
            frequency_penalty=params.get('frequency_penalty', 0.0),
            presence_penalty=params.get('presence_penalty', 0.0)
        )
        
        # Extract response
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        add_to_conversation(channel_id, 'assistant', assistant_message)
        
        return assistant_message
    
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return config.get('response', {}).get('error_message', 
                                               'Sorry, I encountered an error.')


@bot.event
async def on_ready():
    """Event handler for when the bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')


@bot.event
async def on_message(message):
    """Event handler for messages"""
    # Don't respond to own messages
    if message.author == bot.user:
        return
    
    # Check if bot was mentioned
    if bot.user in message.mentions:
        # Remove the mention from the message content
        content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
        
        if not content:
            content = "Hello!"
        
        # Show typing indicator if configured
        if config.get('response', {}).get('typing_indicator', True):
            async with message.channel.typing():
                # Generate response
                response = await generate_response(
                    content, 
                    message.channel.id,
                    message.author.display_name
                )
                
                # Send response
                mention_user = config.get('response', {}).get('mention_user', True)
                if mention_user:
                    await message.reply(response)
                else:
                    await message.channel.send(response)
        else:
            # Without typing indicator
            response = await generate_response(
                content, 
                message.channel.id,
                message.author.display_name
            )
            
            mention_user = config.get('response', {}).get('mention_user', True)
            if mention_user:
                await message.reply(response)
            else:
                await message.channel.send(response)
    
    # Process other commands
    await bot.process_commands(message)


@bot.command(name='clear_history')
async def clear_history(ctx):
    """Clear conversation history for this channel"""
    channel_id = ctx.channel.id
    if channel_id in conversation_history:
        conversation_history[channel_id] = []
        await ctx.send("Conversation history cleared!")
    else:
        await ctx.send("No conversation history to clear.")


@bot.command(name='reload_config')
@commands.has_permissions(administrator=True)
async def reload_config(ctx):
    """Reload configuration from config.yaml (admin only)"""
    global config
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        await ctx.send("Configuration reloaded successfully!")
        logger.info("Configuration reloaded")
    except Exception as e:
        await ctx.send(f"Error reloading configuration: {e}")
        logger.error(f"Error reloading configuration: {e}")


def main():
    """Main function to run the bot"""
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        logger.error("Please create a .env file based on .env.example")
        return
    
    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Error running bot: {e}")


if __name__ == '__main__':
    main()
