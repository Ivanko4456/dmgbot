import json
import DMGbot

with open("config.json", "r") as jsonFile:
    cfg = json.load(jsonFile)

bot = DMGbot.DMGbot()
bot.run(cfg['token'])
