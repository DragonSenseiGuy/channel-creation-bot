import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import storage

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CATEGORY_ID = os.getenv('TARGET_CATEGORY_ID')

# Bot setup
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sync commands globally for simplicity in this example.
        # In production, you might want to sync to a specific guild for faster updates during dev.
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command(name="create-channel", description="Creates a new text channel")
@app_commands.describe(channel_name="The name of the channel to create")
async def create_channel(interaction: discord.Interaction, channel_name: str):
    # Check if user has reached the limit
    user_id = interaction.user.id
    current_count = storage.get_user_channel_count(user_id)
    
    if current_count >= 2:
        await interaction.response.send_message("You have reached the limit of 2 created channels.", ephemeral=True)
        return

    # Get the category
    if not TARGET_CATEGORY_ID:
        await interaction.response.send_message("Configuration error: TARGET_CATEGORY_ID is not set.", ephemeral=True)
        return

    try:
        category = interaction.guild.get_channel(int(TARGET_CATEGORY_ID))
        if not category or not isinstance(category, discord.CategoryChannel):
             # Fallback: try to fetch if get returns None (though get is usually sufficient if cache is ready)
             # For simplicity, we assume cache is populated or we error out.
             await interaction.response.send_message(f"Configuration error: Category with ID {TARGET_CATEGORY_ID} not found.", ephemeral=True)
             return
    except ValueError:
        await interaction.response.send_message("Configuration error: Invalid TARGET_CATEGORY_ID.", ephemeral=True)
        return

    # Create the channel
    try:
        # Defer response since channel creation might take a moment
        await interaction.response.defer(ephemeral=True)
        
        new_channel = await interaction.guild.create_text_channel(name=channel_name, category=category)
        
        # Ping the user in the new channel
        await new_channel.send(f"Channel created {interaction.user.mention}!")

        # Increment count
        storage.increment_user_channel_count(user_id)
        
        await interaction.followup.send(f"Channel {new_channel.mention} created successfully!")
        
    except discord.Forbidden:
        await interaction.followup.send("I do not have permission to create channels in that category.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.followup.send(f"Failed to create channel: {e}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)

if __name__ == '__main__':
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env")
    else:
        client.run(TOKEN)
