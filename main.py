import logging, requests, random, json
from bs4 import BeautifulSoup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def help(update, context):
    update.message.reply_text(
        '/giphy <search> <# times>\n'
        '/pornhub <search>\n'
        '/quote'
        )

def quote(update, context):
    response = requests.get("https://api.quotable.io/random")
    update.message.reply_text(json.loads(response.text)['content']+"\n-"+json.loads(response.text)['author'])

def pornhub(update, context):
    search_keyword = update.message.text.split()[1]

    URL = 'https://www.pornhub.com/video/search?search='
    response = requests.get(URL + search_keyword)
    soup = BeautifulSoup(response.text, 'lxml')
    ph_links = []
    for a in soup.find_all('a', href=True):
        if a['href'].startswith("/view_video"):
            ph_links.append('https://www.pornhub.com' + a['href'])
    update.message.reply_text(random.choice(ph_links))

def giphy(update, context):
    search_keyword = "-".join(update.message.text.split()[1:])
    N = 1
    if update.message.text.split()[-1].isnumeric():
        N = int(update.message.text.split()[-1])
        
    for _ in range(N):
        URL = 'http://api.giphy.com'
        SEARCH_PATH = '/v1/gifs/search'
        payload = {'api_key': 'gKs8c63gf2e6Vq75MlQBWpuW1yCD7TsC', 'q': search_keyword}
        r = requests.get(URL + SEARCH_PATH, params=payload)
        data = r.json()['data']
        image_position = random.randrange(0, len(data))
        image_url = data[image_position]['images']['original']['url']
        update.message.reply_animation(image_url)


def main():
    updater = Updater("5225421589:AAEq4Hr37vkVO4_2YYVTwHSTc6QxhlkD0aU", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("giphy", giphy))
    dp.add_handler(CommandHandler("pornhub", pornhub))
    dp.add_handler(CommandHandler("quote", quote))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
