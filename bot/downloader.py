import os
from logging import getLogger
import urllib.request
from pathlib import Path

import discord
from discord.ext import commands
from helper.twittermanager import TwitterManager
from common.botexception import BotException


class Downloader(commands.Cog):
    """自動通知管理のためのCog.

    Args:
        commands (commands.Cog): 継承元
    """

    def __init__(self, bot: commands.Bot):
        """初期化.

        Args:
            bot (commands.Bot): 参照するBotクラス
        """
        super().__init__()
        self.bot = bot
        self.logger = getLogger("TweetDownloaderLog.Downloader")

        # ダウンロードした画像の格納ディレクトリ
        self.SAVE_DIRECTRY = Path("Downloaded")
        self.SAVE_DIRECTRY.mkdir(exist_ok=True)

        # Twitter設定
        self.twitter = TwitterManager()

        self.logger.info("Downloader初期化完了")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        try:
            self.logger.info(f"Check URL : {message.content}")
            imageurls = self.twitter.get_image_urls(message.content)

            if len(imageurls) > 0:
                self.logger.info(f"Found {len(imageurls)} Image. {message.content}")
            else:
                # 画像が見つからない場合はレスポンスを返しません。
                self.logger.info(f"No Image. {message.content}")
                return

            for url in imageurls:
                self.logger.info(f"Download Start. {url}")
                filename = os.path.basename(url)

                # 同じファイルがダウンロード先にあっても確認せず上書きダウンロードする。
                urllib.request.urlretrieve(url, self.SAVE_DIRECTRY / filename)
                self.logger.info(f"Download finish. {url}")

            await message.channel.send(f"{len(imageurls)} 枚の画像をダウンロードしました。")
        except BotException as e:
            self.logger.error(f"Download Failed. {message.content}")
            await message.channel.send(e)


def setup(bot: commands.Bot):
    """Cogの登録.

    Args:
        bot (commands.Bot): 参照するBotクラス
    """
    bot.add_cog(Downloader(bot))
