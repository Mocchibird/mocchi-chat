"""
Fine-tuning and training utilities for Mocchibird
This module provides utilities for preparing training data and fine-tuning the bot
"""
import json
import os
from typing import List, Dict
from datetime import datetime
import yaml


class TrainingDataPreparer:
    """Class for preparing training data from Discord conversations"""
    
    def __init__(self, output_dir: str = 'training_data'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_training_example(self, user_message: str, bot_response: str, 
                                system_prompt: str = None) -> Dict:
        """
        Create a training example in the format expected by OpenAI fine-tuning
        
        Args:
            user_message: The user's message
            bot_response: The bot's response
            system_prompt: Optional system prompt
            
        Returns:
            A dictionary representing a training example
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        messages.append({
            "role": "assistant",
            "content": bot_response
        })
        
        return {"messages": messages}
    
    def prepare_training_file(self, examples: List[Dict], 
                            filename: str = None) -> str:
        """
        Prepare a JSONL file for fine-tuning
        
        Args:
            examples: List of training examples
            filename: Output filename (default: training_data_TIMESTAMP.jsonl)
            
        Returns:
            Path to the created file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'training_data_{timestamp}.jsonl'
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            for example in examples:
                f.write(json.dumps(example) + '\n')
        
        print(f"Training data saved to {filepath}")
        print(f"Total examples: {len(examples)}")
        
        return filepath
    
    def load_conversations_from_file(self, filepath: str) -> List[Dict]:
        """
        Load conversations from a JSON file
        
        Expected format:
        [
            {
                "user": "Hello!",
                "assistant": "Hi! How can I help you?"
            },
            ...
        ]
        """
        with open(filepath, 'r') as f:
            conversations = json.load(f)
        
        return conversations
    
    def prepare_from_conversations(self, conversations: List[Dict], 
                                   system_prompt: str = None) -> List[Dict]:
        """
        Convert a list of conversations into training examples
        
        Args:
            conversations: List of conversation dictionaries
            system_prompt: Optional system prompt to include
            
        Returns:
            List of training examples
        """
        examples = []
        
        for conv in conversations:
            example = self.create_training_example(
                conv.get('user', ''),
                conv.get('assistant', ''),
                system_prompt
            )
            examples.append(example)
        
        return examples


class ConfigUpdater:
    """Class for updating bot configuration based on training"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load current configuration"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def update_system_prompt(self, new_prompt: str):
        """Update the system prompt in the configuration"""
        self.config['system_prompt'] = new_prompt
        self.save_config()
    
    def update_model_parameters(self, **params):
        """
        Update model parameters
        
        Args:
            **params: Keyword arguments for parameters to update
                     (temperature, max_tokens, top_p, etc.)
        """
        if 'model_parameters' not in self.config:
            self.config['model_parameters'] = {}
        
        for key, value in params.items():
            self.config['model_parameters'][key] = value
        
        self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        print(f"Configuration saved to {self.config_path}")


def create_example_training_data():
    """
    Create an example training data file to demonstrate the format
    """
    preparer = TrainingDataPreparer()
    
    # Example conversations
    conversations = [
        {
            "user": "Hello! What's your name?",
            "assistant": "Hi! I'm Mocchibird, your friendly AI assistant. How can I help you today?"
        },
        {
            "user": "Can you help me with Python programming?",
            "assistant": "Of course! I'd be happy to help with Python programming. What specific topic or problem are you working on?"
        },
        {
            "user": "What can you do?",
            "assistant": "I can help with a variety of tasks including answering questions, providing information, helping with programming, having conversations, and more. Just let me know what you need!"
        },
        {
            "user": "Thank you!",
            "assistant": "You're welcome! Feel free to ask if you need anything else. I'm here to help!"
        }
    ]
    
    # Prepare training examples
    system_prompt = "You are Mocchibird, a friendly and helpful AI assistant."
    examples = preparer.prepare_from_conversations(conversations, system_prompt)
    
    # Save to file
    filepath = preparer.prepare_training_file(examples, 'example_training_data.jsonl')
    
    print(f"\nExample training data created at: {filepath}")
    print("You can use this as a template for your own training data.")
    
    return filepath


def main():
    """
    Main function to demonstrate training data preparation
    """
    print("Mocchibird Training Data Preparation Tool")
    print("=" * 50)
    print()
    print("Choose an option:")
    print("1. Create example training data")
    print("2. Prepare training data from conversations file")
    print("3. Update configuration")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        create_example_training_data()
    
    elif choice == '2':
        filepath = input("Enter path to conversations JSON file: ").strip()
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} not found!")
            return
        
        preparer = TrainingDataPreparer()
        try:
            conversations = preparer.load_conversations_from_file(filepath)
            
            # Load system prompt from config
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
                system_prompt = config.get('system_prompt')
            
            examples = preparer.prepare_from_conversations(conversations, system_prompt)
            preparer.prepare_training_file(examples)
            
        except Exception as e:
            print(f"Error processing file: {e}")
    
    elif choice == '3':
        print("\nConfiguration Update Tool")
        print("1. Update system prompt")
        print("2. Update model parameters")
        
        sub_choice = input("Enter your choice (1-2): ").strip()
        updater = ConfigUpdater()
        
        if sub_choice == '1':
            print("\nCurrent system prompt:")
            print(updater.config.get('system_prompt', 'Not set'))
            print()
            new_prompt = input("Enter new system prompt: ").strip()
            updater.update_system_prompt(new_prompt)
        
        elif sub_choice == '2':
            print("\nCurrent model parameters:")
            print(json.dumps(updater.config.get('model_parameters', {}), indent=2))
            print()
            print("Enter new parameter values (press Enter to skip):")
            
            params = {}
            for param in ['temperature', 'max_tokens', 'top_p', 
                         'frequency_penalty', 'presence_penalty']:
                value = input(f"{param}: ").strip()
                if value:
                    try:
                        params[param] = float(value) if '.' in value else int(value)
                    except ValueError:
                        print(f"Invalid value for {param}, skipping")
            
            if params:
                updater.update_model_parameters(**params)
    
    else:
        print("Invalid choice!")


if __name__ == '__main__':
    main()
