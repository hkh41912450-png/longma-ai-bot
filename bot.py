import os
import discord
from discord.ext import commands

BOT_TOKEN = os.getenv"DISCORD_BOT_TOKEN", "")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

FAQ = {
    "价格": "💳 **价格说明**\n按量计费，无月费。具体联系客服。",
    "模型": "🤖 **支持模型**\nGPT-4o, Claude 3.5, Gemini, DeepSeek, Qwen 等",
    "充值": "💰 **充值方式**\nUSDT / 银行转账",
    "使用": "🔧 **接入方法**\n```python\nimport openai\nclient = openai.OpenAI(\n  api_key=***  base_url=\"https://aigc.x-see.cn/v1\"\n)\n```",
    "试用": "🎁 新人可申请试用额度，联系客服",
}

@bot.event
async def on_ready():
    print(f"✅ Bot 上线: {bot.user}")

@bot.event
async def on_member_join(member):
    ch = discord.utils.get(member.guild.text_channels, name="welcome")
    if ch:
        await ch.send(f"🎉 欢迎 {member.mention} 加入龙马AI！输入 !help 查看指令")

@bot.command(name="help")
async def help_cmd(ctx):
    e = discord.Embed(title="🤖 龙马AI Bot", color=discord.Color.green())
    e.add_field(name="!faq", value="常见问题")
    e.add_field(name="!pricing", value="价格")
    e.add_field(name="!models", value="模型")
    e.add_field(name="!setup", value="教程")
    e.add_field(name="!trial", value="试用")
    e.add_field(name="!contact", value="客服")
    await ctx.send(embed=e)

@bot.command(name="pricing")
async def pricing(ctx): await ctx.send(FAQ["价格"])
@bot.command(name="models")
async def models(ctx): await ctx.send(FAQ["模型"])
@bot.command(name="setup")
async def setup(ctx): await ctx.send(FAQ["使用"])
@bot.command(name="trial")
async def trial(ctx): await ctx.send(FAQ["试用"])
@bot.command(name="contact")
async def contact(ctx): await ctx.send("📞 在 #support 提问或私信管理员")

bot.run(BOT_TOKEN)
