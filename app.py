import json
import asyncio
from type4format import Type4scrappers
# from typeformat2 import BannerCourseScraper 

def mainScrapper(): 
    try:
        with open("type4links.json", "r") as f: 
            data = json.load(f) 

        for key,value in data.items():
            scraper = Type4scrappers(key,value)   
            asyncio.run(scraper.mainscrapper())

    except Exception as e:   
        print("error occured while type4scraping...")     


if __name__=='__main__':
    mainScrapper() 