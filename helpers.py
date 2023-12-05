import json

from price_tracker.commands import Invoker, HepsiburadaCommand, GittigidiyorCommand, TrendyolCommand, AmazonCommand, \
    VatanCommand, TeknosaCommand, N11Command, CiceksepetiNetCommand, CiceksepetiComCommand, MediamarktCommand, \
    EbayCommand, MorhipoCommand, TeknostoreCommand, LetgoCommand, KitapyurduCommand, TozluCommand, DandRCommand, \
    ToyzzshopCommand, NikeCommand
from price_tracker.scraper import Scraper
from price_tracker.constants import PRODUCTS_PATH


def build_invoker(mailer):
    # Reading product list
    try:
        with open(PRODUCTS_PATH) as json_file:
            products = json.load(json_file)
    except FileNotFoundError:
        print("Products file couldn't be found")
        exit(3)
    except ValueError:
        print('Products file is broken')
        exit(3)

    # Scraper instance that is receiver of commands
    scraper = Scraper(mailer)

    # Creating an invoker for the execute remaining commands
    invoker = Invoker()
    for product in products:
        invoker.register(build_command(scraper, product))

    return invoker


# Function for generating commands from domain address
def build_command(receiver, item):
    if 'hepsiburada' in item['url']:
        return HepsiburadaCommand(receiver, item)
    elif 'gittigidiyor' in item['url']:
        return GittigidiyorCommand(receiver, item)
    elif 'trendyol' in item['url']:
        return TrendyolCommand(receiver, item)
    elif 'amazon' in item['url']:
        return AmazonCommand(receiver, item)
    elif 'vatanbilgisayar' in item['url']:
        return VatanCommand(receiver, item)
    elif 'teknosa' in item['url']:
        return TeknosaCommand(receiver, item)
    elif 'n11' in item['url']:
        return N11Command(receiver, item)
    elif 'ciceksepeti.net' in item['url']:
        return CiceksepetiNetCommand(receiver, item)
    elif 'ciceksepeti.com' in item['url']:
        return CiceksepetiComCommand(receiver, item)
    elif 'mediamarkt' in item['url']:
        return MediamarktCommand(receiver, item)
    elif 'ebay' in item['url']:
        return EbayCommand(receiver, item)
    elif 'morhipo' in item['url']:
        return MorhipoCommand(receiver, item)
    elif 'teknostore' in item['url']:
        return TeknostoreCommand(receiver, item)
    elif 'letgo' in item['url']:
        return LetgoCommand(receiver, item)
    elif 'kitapyurdu' in item['url']:
        return KitapyurduCommand(receiver, item)
    elif 'tozlu' in item['url']:
        return TozluCommand(receiver, item)
    elif 'dr.com' in item['url']:
        return DandRCommand(receiver, item)
    elif 'toyzzshop' in item['url']:
        return ToyzzshopCommand(receiver, item)
    elif 'decathlon' in item['url']:
        return ToyzzshopCommand(receiver, item)
    elif 'nike.com' in item['url']:
        return NikeCommand(receiver, item)
    else:
        print(f'{item["url"]} is a non-supported web site')
