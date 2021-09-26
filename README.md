# tweetimagedownloaderbot
Tweetに画像が含まれていたらローカルPCにダウンロードするBot

## 動作確認環境

* Windows
  * Windows10 64bit 21H1
  * Python : 3.9.5
  * discord.py : 1.7.3
  * poetry : 1.1.5
  * git : 2.27.0
* Raspberry Pi
  * Raspbian GNU/Linux 10 (buster)
  * Python : 3.9.5
  * discord.py : 1.7.3
  * poetry : 1.1.6
  * git : 2.20.1

## 初期設定

1. pythonとpoetry, gitをあらかじめインストールしておく。
2. github上のファイルをダウンロードし、任意の位置に格納する。(git cloneでも可)
3. pyproject.tomlがあるディレクトリ上で下記を実行し、動作に必要なソフトウェアをインストールする。

   ```
   poetry install --no-dev
   ```

4. Discord Botと Twitter API のアクセストークン一式を取得する。
   * Discord Botの権限
     * Scopes : bot のみチェック
     * Bot Permissions : View Channels と Send Messages をチェック
5. 環境変数 として 下記を登録する。
   * IMAGEBOT_TOKEN : Discord Bot のトークン
   * TWITTER_API_KEY : Twitter API Key 
   * TWITTER_API_SECRET : Twitter API SECRET 
   * TWITTER_ACCESS_TOKEN : Twitter アクセストークン 
   * TWITTER_ACCESS_TOKEN_SECRET : Twitter アクセストークン SECRET


## 起動方法

1. pyproject.tomlがあるディレクトリ上で下記コマンドを実行しBotを起動する。
   * 初期設定の項目がすべて完了していない場合、Botは正常起動しません。

   ```
   python3 bot.py
   ```

## 使用方法

* Botがメッセージを参照できる権限を持つチャンネル内で、TwitterのツイートURLを書き込む。
  * ツイート情報から画像URLがないか確認し、URLが存在すればローカルPCにダウンロードする。
    * ダウンロード先はカレントディレクトリ直下のDownloadedディレクトリ内
    * 保存ファイル名はTweet上のファイル名

## 制限事項

* 画像を含むツイートであっても、URLが取り出せない場合はダウンロードが実行されません。

## その他

* 実行時のログはカレントディレクトリ直下のLogsディレクトリに、逐次記録。
  * ファイル名は log{Bot起動時刻}.log


## ライセンス

MIT License
