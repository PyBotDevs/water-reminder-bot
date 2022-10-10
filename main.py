### NKA (aka. PyBotDevs) 2022. For enquiries contact <pybotdevs@outlook.com> ###

# Imports
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.ext.commands import *
# import os
import os.path
import time
# from time import strftime
import datetime
import math
from framework.isobot.colors import Colors
import json
import asyncio
from threading import Thread

# Configuration
client = commands.Bot(command_prefix='w!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
start_time = math.floor(time.time())
start_timestamp = datetime.datetime.now()
colors = Colors()
theme_color = discord.Color.blue()
wdir = os.getcwd()
with open('database/users.json', 'r') as f: users = json.load(f)
print(f"[main/database] Databases successfully loaded")


# Functions
def save():
    with open('database/users.json', 'w+') as f: json.dump(users, f, indent=4)
    print(f"[main/database] {colors.green}Database save request complete{colors.end}")


# Classes
class ReminderDaemon:
    def __init__(self):
        self.reminders = list()
        print(f"[ReminderDaemon/starter] {colors.green}ReminderDaemon successfully initialized.{colors.end}")

    async def start_reminder_daemon(self):
        print(f"[ReminderDaemon/starter] {colors.green}ReminderDaemon successfully started!{colors.end}")
        try:
            daemon = Thread(target=await self.start_all_reminders())
            daemon.run()
        except RuntimeError:
            daemon = Thread(target=await self.start_all_reminders())
            daemon.run()

    async def start_reminder(self, user_id: int, interval: int):
        self.reminders.append(str(user_id))
        while str(user_id) in self.reminders:
            await asyncio.sleep(interval)
            user_data = client.get_user(user_id)
            localembed = discord.Embed(title="It's time to drink water!", description="Grab a glass or water bottle, and hydrate yourself!", color=theme_color)
            await user_data.send(embed=localembed)

    async def stop_reminder(self, user_id: int):
        self.reminders.remove(str(user_id))

    async def start_all_reminders(self):
        for x in users:
            await self.start_reminder(int(x), users[str(x)]["water_reminder"]["interval"])


# Class Initialization
reminder_daemon = ReminderDaemon()


# Events
@client.event
async def on_ready():
    print(f"[main/startup] {colors.green}Logged in as {client.user.name}.{colors.end}")
    print(f"[main/startup] {colors.green}Ready to accept commands.{colors.end}")
    print(f"[main/startup] Client ready in {math.floor(time.time()) - start_time} sec; Client latency is {round(client.latency, 2)} ms")
    try: await reminder_daemon.start_reminder_daemon()
    except RuntimeError: await reminder_daemon.start_reminder_daemon()


# Commands
@slash.slash(
    name="subscribe",
    description="Sets up automatic water reminders for you"
)
async def subscribe(ctx: SlashContext):
    print(f"[main/command client] /subscribe command invoked by user")
    if str(ctx.author.id) in users: return await ctx.reply("You are already subscribed to water reminders!", hidden=True)
    users[str(ctx.author.id)] = {
        "water_reminder": {
            "active": True,
            "time_subscribed": math.floor(time.time()),
            "interval": 7200
        }
    }
    save()
    localembed = discord.Embed(title=":potable_water: Your water reminder is set!", description="We will now remind you every 2 hours to drink water.\nIf you ever want to cancel these reminders, you can type `/unsubscribe`.", color=theme_color)
    await ctx.reply(embed=localembed)
    await reminder_daemon.start_reminder(ctx.author.id, 7200)


@slash.slash(
    name="subscription_list",
    description="Shows what reminders you are currently subscribed to"
)
async def subscription_list(ctx: SlashContext):
    print(f"[main/command client] /subscription_list command invoked by user")
    localembed = discord.Embed(title="Your subscription list", color=theme_color)
    if str(ctx.author.id) in users:
        if users[str(ctx.author.id)]["water_reminder"]["active"] is True: localembed.add_field(name="Water Reminders", value="Currently Subscribed")
        elif users[str(ctx.author.id)]["water_reminder"]["active"] is False: localembed.add_field(name="Water Reminders", value="Subscription Paused")
    else: localembed.add_field(name="Water Reminders", value="Not Subscribed")
    await ctx.send(embed=localembed)


@slash.slash(
    name="unsubscribe",
    description="Stops sending automatic water reminders to you"
)
async def unsubscribe(ctx: SlashContext):
    print(f"[main/command client] /unsubscribe command invoked by user")
    if str(ctx.author.id) not in users: return await ctx.reply("Oops! Looks like you aren't subscribed to water reminders yet! (you can subscribe using `/subscribe` command)", hidden=True)
    del users[str(ctx.author.id)]
    save()
    await reminder_daemon.stop_reminder(ctx.author.id)
    localembed = discord.Embed(title=":broken_heart: You have successfully unsubscribed from water reminders!", description="You will not be sent frequent reminders to drink water anymore.\nHowever, you can always subscribe back by using the `/subscribe` command!")
    await ctx.reply(embed=localembed)


# @slash.slash(
#     name="pause_subscription",
#     description="Temporarily pauses your automatic water reminders"
# )
# async def pause_subscription(ctx: SlashContext):
#     print(f"[main/command client] /pause_subscription command invoked by user")
#     if str(ctx.author.id) not in users: return await ctx.reply("Oops! Looks like you aren't subscribed to water reminders yet! (you can subscribe using `/subscribe` command)", hidden=True)
#     if users[str(ctx.author.id)]["water_reminder"]["active"] is False: return await ctx.reply("Your water reminders are already paused.", hidden=True)
#     users[str(ctx.author.id)]["water_reminder"]["active"] = False
#     save()
#     localembed = discord.Embed(title=":pause_button: Your water reminders have been paused!", description="Whenever you want to, you can resume your water reminders with `/resume_subscription`.", color=discord.Color.light_grey())
#     await ctx.send(embed=localembed)


# @slash.slash(
#     name="resume_subscription",
#     description="Resumes your automatic water reminders"
# )
# async def resume_subscription(ctx: SlashContext):
#     print(f"[main/command client] /resume_subscription command invoked by user")
#     if str(ctx.author.id) not in users: return await ctx.reply("Oops! Looks like you aren't subscribed to water reminders yet! (you can subscribe using `/subscribe` command)", hidden=True)
#     if users[str(ctx.author.id)]["water_reminder"]["active"] is True: return await ctx.reply("Your water reminders are already active.", hidden=True)
#     users[str(ctx.author.id)]["water_reminder"]["active"] = True
#     save()
#     localembed = discord.Embed(title=":arrow_forward: Your water reminders have been resumed!", description="You will now start receiving automatic water reminders again!", color=discord.Color.green())
#     await ctx.send(embed=localembed)


@slash.slash(
    name="status",
    description="Shows the current bot status, along with a few other details"
)
async def status(ctx: SlashContext):
    print(f"[main/command client] /status command invoked by user")
    localembed = discord.Embed(title="Bot status", color=theme_color)
    localembed.add_field(name="Current Latency (ping)", value=f"{round(client.latency, 2)} ms")
    localembed.add_field(name="Client Startup Time", value=f"{math.floor(time.time()) - start_time} seconds")
    localembed.add_field(name="Time Started", value=start_timestamp.strftime("%H:%M:%S on %d/%m/%Y"))
    await ctx.send(embed=localembed)


@slash.slash(
    name="set_reminder_interval",
    description="Sets a specified water reminder interval for you",
    options=[
        create_option(name="interval", description="How often do you want us to remind you to drink water?", option_type=str, required=True, choices=["30 minutes", "1 hour", "1.5 hours", "2 hours", "3 hours"])
    ],
)
async def set_reminder_interval(ctx: SlashContext, interval: str):
    print(f"[main/command client] /set_reminder_interval command invoked by user")
    if str(ctx.author.id) not in users: return await ctx.reply("Oops! Looks like you aren't subscribed to water reminders yet! (you can subscribe using `/subscribe` command)", hidden=True)
    secs = int()
    if interval == "30 minutes": secs = 60*30
    elif interval == "1 hour": secs = 60*60
    elif interval == "1.5 hours": secs = 60*90
    elif interval == "2 hours": secs = 60*120
    elif interval == "3 hours": secs = 60*180
    users[str(ctx.author.id)]["water_reminder"]["interval"] = secs
    save()
    await reminder_daemon.stop_reminder(ctx.author.id)
    time.sleep(0.1)
    localembed = discord.Embed(title=":white_check_mark: Interval set!", description=f"We will now remind you every {interval} to drink water!", color=theme_color)
    await ctx.send(embed=localembed)
    await reminder_daemon.start_reminder(ctx.author.id, int(users[str(ctx.author.id)]["water_reminder"]["interval"]))


# Client Initialization
print(f"[main/startup] Connecting to Discord API...")
try: client.run("")  # The bot token goes here (inside the "")
except Exception as exc: print(f"[main/startup] {colors.red}Connection failed: {exc}{colors.end}")