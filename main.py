import json
import DMGbot

with open("config.json", "r") as jsonFile:
    cfg = json.load(jsonFile)

if __name__ == '__main__':
    bot = DMGbot.DMGbot()
    bot.run(cfg['token'])
