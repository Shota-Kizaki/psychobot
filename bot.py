import discord
from discord.ext import commands
import re
from sudachipy import tokenizer
from sudachipy import dictionary
import markovify
import hoge
from dotenv import load_dotenv
load_dotenv()

import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

TOKEN = os.getenv('token')

# ファイルを読み込んでテキストを結合する関数
def load_files(files):
    text = ''
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text += f.read().strip()  # ファイルの内容を読み込んで結合
    return text

# テキストの前処理を行う関数
def preprocess_text(text):
    tokenizer_obj = dictionary.Dictionary().create()  # Sudachiの辞書を使用
    mode = tokenizer.Tokenizer.SplitMode.C
    words = [m.surface() for m in tokenizer_obj.tokenize(text, mode)]  # テキストを単語に分割

    cleaned_text = ''
    for word in words:
        # 特定の記号や空白を削除
        word = re.sub(r'[（）「」『』｛｝【】＠”’！？｜～・()\[\]{}@\'\"!?|~-]', '', word)
        word = re.sub(r'\u3000', '', word)  # 全角スペースを削除
        word = re.sub(r'[ \n]', '', word)   # 半角スペースや改行を削除
        word = re.sub(r'。', '。\n', word)  # 句点を改行付きの句点に置換
        cleaned_text += word + ' '  # 結合した単語を追加
    return cleaned_text

# 文章を生成する関数
def generate_sentence(exec_times, text_model):
    combined_sentence = ''
    for i in range(exec_times):
        # マルコフ連鎖を使用して文章を生成
        sentence = text_model.make_short_sentence(100, tries=100, max_words=400)
        if sentence:  # Noneでない場合に追加
            combined_sentence += sentence + ' '  # 文章を結合
    return combined_sentence.strip()  # 不要な空白を削除して返す

# メッセージ受信時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました\n---------------------------------------')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author == bot.user:
        return
    # 「/gag」と発言したらサイコパスな恋文を返します
    if message.content == '/gag':
        input_text = hoge.hoge() # ファイルからテキストを読み込む
        splitted_text = preprocess_text(input_text)  # テキストの前処理を行う
        text_model = markovify.NewlineText(splitted_text, state_size=3)  # マルコフ連鎖のモデルを構築
        sentence = generate_sentence(5, text_model)  # 文章を生成
        sentence = sentence.replace(' ', '')  # スペースを削除
        henzi = '愛しい君へ、\n\n' + sentence + '\n\n心からではないが、 存在Xより。'  # ヘンジを構築
        print(henzi)  # ヘンジを出力
        print('---------------------------------------')
        await message.channel.send(henzi)  # チャンネルにヘンジを送信

# Botの起動
bot.run(TOKEN)
