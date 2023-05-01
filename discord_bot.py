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

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Discord client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
#https://discord.com/api/oauth2/authorize?client_id=1100429021944225902&permissions=345744992320&scope=bot

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

# Define function to handle messages sent to the Discord server
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Generate response using ChatGPT3.5
    input_text = message.content
    response = generate_response(input_text)

    # Send response back to Discord server
    await message.channel.send(response)

# Run the Discord client
client.run(DISCORD_TOKEN)
