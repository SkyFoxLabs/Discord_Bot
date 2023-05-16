#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 18:57:47 2023

@author: petercalimlim
"""

import discord
import openai
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Discord token from environment variable
discord_token = os.getenv('DISCORD_TOKEN')

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Dictionary to store conversation history and last active time for each user
conversation_history = {}
last_active_time = {}

# Inactive time limit (5 minutes)
inactive_time_limit = timedelta(minutes=5)

@client.event
async def on_ready():
    print('Bot is ready and connected to Discord.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id

    if message.content.lower() == 'quit':
        if user_id in conversation_history:
            # Remove the conversation history and last active time for the user
            del conversation_history[user_id]
            del last_active_time[user_id]
        await message.channel.send("Chat session ended. You can start a new session anytime.")
        return

    if user_id in conversation_history:
        # Update the last active time for the user
        last_active_time[user_id] = datetime.now()

        # Append the new message to the existing conversation history
        conversation_history[user_id].append(message.content)
    else:
        # Start a new conversation history and set the last active time for the user
        conversation_history[user_id] = [message.content]
        last_active_time[user_id] = datetime.now()

    # Concatenate the conversation history for the user with newline separator
    conversation = "\n".join(conversation_history[user_id])

    # Generate response using conversation history
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=conversation,
        max_tokens=100
    )

    bot_response = response.choices[0].text.strip()
    await message.channel.send(bot_response)

    # Check inactive time limit
    if (datetime.now() - last_active_time[user_id]) >= inactive_time_limit:
        await message.channel.send("It seems you have been inactive. If you want to continue, please type a message.")

        try:
            # Wait for the user's response for a maximum of 2 minutes
            continue_message = await client.wait_for('message', timeout=120, check=lambda m: m.author.id == user_id)
        except asyncio.TimeoutError:
            # If no response from the user, end the session and delete conversation context
            del conversation_history[user_id]
            del last_active_time[user_id]
            await message.channel.send("Chat session ended due to inactivity.")
            return
        
        # Update the conversation history and last active time with the user's response
        conversation_history[user_id].append(continue_message.content)
        last_active_time[user_id] = datetime.now()


client.run(discord_token)
