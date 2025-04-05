# 导入所需库（网页[4]推荐方式）
import telebot
from config import token  # 从配置文件导入机器人令牌
import random
import logging
import time
from telebot import types  # 引入Telegram类型系统
import os

# 配置下载目录常量（网页[6]路径管理方案）
DOWNLOADS_DIR = "downloads"

# 初始化机器人实例（网页[8]标准做法）
bot = telebot.TeleBot(token)

# 配置基础日志记录（网页[6]错误处理建议）
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 处理 /start 命令（网页[4]基础命令示例）
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """发送欢迎信息"""
    welcome_text = """\
你好，我是测试机器人！
使用 /help 查看可用命令
"""
    bot.reply_to(message, welcome_text)

# 处理 /help 命令（网页[8]帮助系统实现）
@bot.message_handler(commands=['help'])
def send_help(message):
    """显示帮助菜单"""
    help_text = """\
可用命令：
/poll - 创建编程测试投票
/username - 获取用户名
趣味功能：
/altf4 - 经典玩笑
/system32 - 系统梗图
/downloadavatar - 下载头像（开发中）
/avatar - 头像功能
/game - 数字猜谜游戏
/random - 随机发送媒体文件
"""
    bot.reply_to(message, help_text)

# 处理 /altf4 玩笑命令（网页[8]趣味功能示例）
@bot.message_handler(commands=['altf4'])
def send_altf4message(message):
    """经典Alt+F4玩笑"""
    response = """\
机器人：*alt+f4*
机器人：不过我是机器人，这招对我无效😉
"""
    bot.reply_to(message, response, parse_mode='Markdown')

# 处理 /system32 命令（网页[4]媒体发送示例）
@bot.message_handler(commands=['system32'])
def send_jokesystem32meme(message):
    """发送系统梗图"""
    try:
        with open('badpiggies.jpg', 'rb') as photo:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption='禁止删除系统文件❗️'
            )
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ 图片文件未找到")

# 创建投票功能（网页[4]高级功能实现）
@bot.message_handler(commands=["poll"])
def create_poll(message):
    """创建编程测试投票"""
    question = "以下代码使用什么语言？\nusing System.IO;\nusing System.Windows.Forms;"
    options = ["Python", "Java", "C#", "C++"]
    
    bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        type="quiz",  # 设置为测验模式
        correct_option_id=2,  # C# 是正确答案
        is_anonymous=False,  # 显示参与者
        explanation="正确答案是C#，属于.NET框架语法"  # 网页[8]功能扩展
    )

# 投票结果处理（网页[6]回调处理示例）
@bot.poll_answer_handler()
def handle_poll(poll):
    """处理投票结果"""
    user_id = poll.user.id
    selected = poll.option_ids[0]
    correct = 2  # C# 的选项索引
    
    reaction = "✅" if selected == correct else "❌"
    bot.send_message(user_id, reaction)

# 游戏全局设置
MAX_ATTEMPTS = 7  # 最大尝试次数
user_data = {}  # 存储游戏状态（网页[8]数据管理方案）

@bot.message_handler(commands=['game'])
def start_game(message):
    """启动猜数字游戏"""
    chat_id = message.chat.id
    user_data[chat_id] = {
        'number': random.randint(1, 100),
        'attempts': 0
    }
    bot.send_message(
        chat_id,
        f"🎮 已生成1-100的随机数，你有{MAX_ATTEMPTS}次猜测机会！"
    )

@bot.message_handler(func=lambda msg: msg.chat.id in user_data)
def guess_number(message):
    """处理游戏猜测"""
    chat_id = message.chat.id
    try:
        guess = int(message.text)
        game = user_data[chat_id]
        game['attempts'] += 1

        if guess < game['number']:
            hint = "⬆️ 猜大一点"
        elif guess > game['number']:
            hint = "⬇️ 猜小一点"
        else:
            bot.send_message(
                chat_id,
                f"🎉 恭喜！你在{game['attempts']}次内猜中了！\n/newgame 开始新游戏"
            )
            del user_data[chat_id]
            return

        if game['attempts'] >= MAX_ATTEMPTS:
            bot.send_message(
                chat_id,
                f"游戏结束！正确答案是 {game['number']}\n/newgame 重新开始"
            )
            del user_data[chat_id]
        else:
            remaining = MAX_ATTEMPTS - game['attempts']
            bot.send_message(
                chat_id,
                f"{hint}\n剩余次数：{remaining}次"
            )
    except ValueError:
        bot.send_message(chat_id, "⚠️ 请输入有效数字")


# 新增随机媒体命令（综合网页[3][4][7]实现）
@bot.message_handler(commands=['random'])
def send_random_media(message):
    """随机发送媒体文件功能"""
    try:
        # 获取媒体文件列表（网页[4]目录遍历方法）
        media_files = [
            f for f in os.listdir(DOWNLOADS_DIR)
            if f.lower().endswith(('.jpg', '.gif'))
        ]
        
        if not media_files:
            bot.reply_to(message, "⚠️ 未找到可用媒体文件")
            return
            
        # 随机选择文件（网页[7]随机算法应用）  
        selected_file = random.choice(media_files)
        file_path = os.path.join(DOWNLOADS_DIR, selected_file)
        
        # 根据类型发送文件（网页[3]媒体处理建议）
        with open(file_path, 'rb') as file:
            if selected_file.lower().endswith('.gif'):
                bot.send_animation(
                    chat_id=message.chat.id,
                    animation=file,
                    caption="🎲 随机GIF动画"
                )
            else:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=file,
                    caption="🎲 随机图片"
                )
                
    except FileNotFoundError:
        # 网页[6]错误处理规范
        logging.error(f"下载目录不存在: {DOWNLOADS_DIR}")
        bot.reply_to(message, "❌ 系统配置错误")
    except PermissionError:
        logging.warning(f"目录访问被拒绝: {DOWNLOADS_DIR}")
        bot.reply_to(message, "🔒 文件访问权限不足")
    except Exception as e:
        # 网页[7]异常处理建议
        logging.error(f"媒体发送失败: {str(e)}")
        bot.reply_to(message, "⛔ 媒体加载异常")


# 启动机器人（网页[4]标准启动方式）
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info("机器人启动...")
    bot.infinity_polling()