import asyncio
import random
import re
import os

import aiofiles
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
    command_prefix="!",
    allowed_mentions=discord.AllowedMentions(
        everyone=False,
        users=True,
        roles=False
    )
)


def is_dt():
    def predicate(ctx):
        return ctx.message.author.id == 105726563776999424
    return commands.check(predicate)


@bot.event
async def on_command_error(ctx, error):
    await ctx.message.remove_reaction('⌚', ctx.bot.user)
    await ctx.message.add_reaction("❌")
    await ctx.reply(f"```{error}```")
    raise error


@bot.event
async def on_command(ctx):
    await ctx.message.add_reaction('⌚')


@bot.event
async def on_command_completion(ctx):
    await ctx.message.add_reaction('✅')
    await ctx.message.remove_reaction('⌚', ctx.bot.user)


@bot.command()
@commands.check_any(is_dt(), commands.is_owner())
async def update(ctx, question_set, filetype):
    if ctx.message.attachments:
        await ctx.message.attachments[0].save(os.path.join('data', f"{question_set}_{filetype}.txt"))
        await ctx.reply(f"{filetype} for {question_set} updated successfully.")
    else:
        await ctx.reply("No attachment found.")


@bot.command()
async def gentest(ctx):
    questions = await parsefile("gentest_question.txt")
    question_id = random.choice(list(questions.keys()))
    try:
        await ctx.reply(f"Question gentest #{question_id}:\n\n{questions[question_id]}\n\n`!genanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def genquestion(ctx, question_id: int):
    questions = await parsefile("gentest_question.txt")
    try:
        await ctx.reply(f"Question gentest #{question_id}:\n\n{questions[question_id]}\n\n`!genanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def genanswer(ctx, question_id: int):
    answer = await parsefile("gentest_answer.txt")
    try:
        await ctx.reply(f"Answer for gentest question #{question_id}:\n\n{answer[question_id]}")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def airtest(ctx):
    questions = await parsefile("airtest_question.txt")
    question_id = random.choice(list(questions.keys()))
    try:
        await ctx.reply(f"Question airtest #{question_id}:\n\n{questions[question_id]}\n\n`!airanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def airquestion(ctx, question_id: int):
    questions = await parsefile("airtest_question.txt")
    try:
        await ctx.reply(f"Question airtest #{question_id}:\n\n{questions[question_id]}\n\n`!airanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def genoral(ctx):
    questions = await parsefile("genoral_question.txt")
    question_id = random.choice(list(questions.keys()))
    try:
        await ctx.reply(f"Question genoral #{question_id}:\n\n{questions[question_id]}\n\n`!genoralanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def genoralquestion(ctx, question_id: int):
    questions = await parsefile("genoral_question.txt")
    try:
        await ctx.reply(f"Question genoral #{question_id}:\n\n{questions[question_id]}\n\n`!genoralanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def genoralanswer(ctx, question_id: int):
    answer = await parsefile("genoral_answer.txt")
    try:
        await ctx.reply(f"Answer for genoral question #{question_id}:\n\n{answer[question_id]}")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def airoral(ctx):
    questions = await parsefile("airoral_question.txt")
    question_id = random.choice(list(questions.keys()))
    try:
        await ctx.reply(f"Question airoral #{question_id}:\n\n{questions[question_id]}\n\n`!airoralanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def airoralquestion(ctx, question_id: int):
    questions = await parsefile("airoral_question.txt")
    try:
        await ctx.reply(f"Question airoral #{question_id}:\n\n{questions[question_id]}\n\n`!airoralanswer {question_id}` to get answer.")
    except KeyError:
        await ctx.reply("That question id does not exist.")


@bot.command()
async def airoralanswer(ctx, question_id: int):
    answer = await parsefile("airoral_answer.txt")
    try:
        await ctx.reply(f"Answer for airoral question #{question_id}:\n\n{answer[question_id]}")
    except KeyError:
        await ctx.reply("That question id does not exist.")


async def parsefile(filename):
    d = {}

    async with aiofiles.open(os.path.join('data', filename), errors='ignore') as f:
        content = await f.readlines()

    for c in content:
        if (res := re.search(".([0-9]*)\.\ (.*)", c)) is not None:
            d[int(res.groups()[0])] = res.groups()[1]

    return d


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(os.environ.get("DISCORD_TOKEN")))
    loop.run_forever()
