import os
from logging import getLogger
from typing import Any, List
import traceback

from urllib.parse import urlparse
from tweepy import OAuthHandler, API
from tweepy.errors import TweepyException
import tweepy

from common.botexception import BotException


class TwitterManager:
    """twitterに関する処理の管理."""

    def __init__(self):
        """初期化."""
        self.logger = getLogger("TweetDownloaderLog.TwitterManager")

        auth: Any = OAuthHandler(
            consumer_key=os.environ["FUMIBOT_API_KEY"],
            consumer_secret=os.environ["FUMIBOT_API_SECRET"],
        )

        auth.set_access_token(
            key=os.environ["FUMIBOT_ACCESS_TOKEN"],
            secret=os.environ["FUMIBOT_ACCESS_TOKEN_SECRET"],
        )
        self.twitter: tweepy.API = API(auth)

    def tweet(self, message: str):
        """ツイートする.

        Args:
            message (str): ツイートするメッセージ(140文字未チェック)
        """
        try:
            self.twitter.update_status(message)
        except TweepyException as e:
            self.logger.info("Error: Tweet is Failed.")
            raise e

    def tweetMedia(self, message: str, url: str):
        """ツイートする.

        Args:
            message (str): ツイートするメッセージ(140文字未チェック)
        """
        try:
            self.twitter.update_with_media(url, message)
        except TweepyException as e:
            self.logger.info("Error: TweetMedia is Failed.")
            raise e

    def get_image_urls(self, url: str):
        try:
            tweetid = self.get_tweetid(url)
            id_list = []
            id_list.append(tweetid)
            tweets: List[tweepy.Status] = self.twitter.lookup_statuses(id_list)

            mediaurl_list = []
            for tweet in tweets:
                if hasattr(tweet, "extended_entities"):
                    for media in tweet.extended_entities["media"]:
                        mediaurl_list.append(media["media_url"])
                else:
                    raise BotException(
                        "ツイートURLが入力されましたが、画像が見つからなかったため、ダウンロードは実行されませんでした。"
                    )

            return mediaurl_list
        except TweepyException:
            self.logger.error(f"getTweet is Failed. {url}")
            self.logger.error(traceback.format_exc())
            raise BotException("Tweepyのエラーが発生しました。")
        except AttributeError:
            self.logger.error(f"Tweet Analysis Failed. {url}")
            self.logger.error(traceback.format_exc())
            raise BotException("画像取得に失敗しました。\n特殊な措置が入っている可能性があるため、手動ダウンロードを検討ください。")

    def get_tweetid(self, url: str):
        parse = urlparse(url)

        if parse.netloc == "twitter.com":
            index = parse.path.rfind("/")
            if index >= 0:
                tweetid = parse.path[index + 1 :]
                return tweetid
            else:
                self.logger.info(f"Not Found Tweet ID. {url}")
        else:
            self.logger.info(f"URL is not Tweet. {url}")

        return ""
