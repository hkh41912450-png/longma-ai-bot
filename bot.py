import os
import discord
from discord.ext import commands
import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("bot")

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

if not BOT_TOKEN:
    logger.error("❌ DISCORD_BOT_TOKEN 环境变量未设置！")
    exit(1)

logger.info(f"✅ Token 已读取，长度: {len(BOT_TOKEN)}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

FAQ = {
    "价格": "💳 **价格说明**\n按量计费，无月费。具体联系客服。",
    "模型": "🤖 **支持模型**\nGPT-4o, Claude 3.5, Gemini, DeepSeek, Qwen 等",
    "充值": "💰 **充值方式**\nUSDT / 银行转账",
    "使用": '🔧 **接入方法**\n```python\nimport openai\nclient = openai.OpenAI(\n  api_key=os.getenv("API_KEY"),\n  base_url="https://aigc.x-see.cn/v1"\n)\n```',
    "试用": "🎁 新人可申请试用额度，联系客服",
}

@bot.event
async def on_ready():
    logger.info(f"✅ Bot 上线: {bot.user}")
    logger.info(f"✅ 已连接服务器: {[g.name for g in bot.guilds]}")
    logger.info(f"✅ 服务器数: {len(bot.guilds)}")

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

# 健康检查 HTTP - 在单独的线程里运行，让 Railway 知道进程活着
def run_health_server():
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    logger.info(f"✅ 健康检查服务已启动: 端口 {port}")
    server.serve_forever()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running")
    def log_message(self, format, *args):
        pass  # 不输出 HTTP 日志

if __name__ == "__main__":
    try:
        # 启动健康检查线程
        t = threading.Thread(target=run_health_server, daemon=True)
        t.start()
        # 运行 Bot
        bot.run(BOT_TOKEN)
    except Exception as e:
        logger.error(f"❌ Bot 异常退出: {e}", exc_info=True)
        exit(1)
