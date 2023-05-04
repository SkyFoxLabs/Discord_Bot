#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 18:57:47 2023

@author: petercalimlim
"""

import os
import discord
import openai
from dotenv import load_dotenv
from discord_slash import SlashCommand, SlashContext

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Discord client and slash commands
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY
model_engine = "text-babbage-001"

# Define function to generate response using ChatGPT3.5
def generate_response(input_text):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=input_text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Define slash command to trigger the chatbot response
@slash.slash(name="chat", description="Get a response from the chatbot", guild_ids=[YOUR_SERVER_ID])
async def chat(ctx: SlashContext, message: str):
    # Generate response using ChatGPT3.5
    response = generate_response(message)

    # Send response back to Discord server
    await ctx.send(response)

# Run the Discord client
client.run(DISCORD_TOKEN)
