import abc


class ICommand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self):
        pass


class HepsiburadaCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_hepsiburada_product(self.arg['url'], self.arg['warn_price'])


class GittigidiyorCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_gittigidiyor_product(self.arg['url'], self.arg['warn_price'])


class TrendyolCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_trendyol_product(self.arg['url'], self.arg['warn_price'])


class AmazonCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_amazon_product(self.arg['url'], self.arg['warn_price'])


class VatanCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_vatan_product(self.arg['url'], self.arg['warn_price'])


class TeknosaCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_teknosa_product(self.arg['url'], self.arg['warn_price'])


class N11Command(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_n11_product(self.arg['url'], self.arg['warn_price'])


class CiceksepetiNetCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_ciceksepeti_net_product(self.arg['url'], self.arg['warn_price'])


class CiceksepetiComCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_ciceksepeti_com_product(self.arg['url'], self.arg['warn_price'])


class MediamarktCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_mediamarkt_product(self.arg['url'], self.arg['warn_price'])


class EbayCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_ebay_product(self.arg['url'], self.arg['warn_price'])


class MorhipoCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_morhipo_product(self.arg['url'], self.arg['warn_price'])


class TeknostoreCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_teknostore_product(self.arg['url'], self.arg['warn_price'])


class LetgoCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_letgo_product(self.arg['url'], self.arg['warn_price'])


class KitapyurduCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_kitapyurdu_product(self.arg['url'], self.arg['warn_price'])


class TozluCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_tozlu_product(self.arg['url'], self.arg['warn_price'])


class DandRCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_dandr_product(self.arg['url'], self.arg['warn_price'])


class ToyzzshopCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_toyzzshop_product(self.arg['url'], self.arg['warn_price'])


class DecathlonCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_decathlon_product(self.arg['url'], self.arg['warn_price'])


class NikeCommand(ICommand):
    def __init__(self, receiver, arg):
        self.receiver = receiver
        self.arg = arg

    def execute(self):
        return self.receiver.check_nike_product(self.arg['url'], self.arg['warn_price'])


class Invoker:
    def __init__(self):
        self.commands = []

    def register(self, command):
        self.commands.append(command)

    def clear(self):
        self.commands.clear()

    def is_empty(self):
        if not self.commands:
            return True
        return False

    def execute(self):
        remaining_list = []
        for command in self.commands:
            try:
                res = command.execute()
            except AttributeError:
                print(f"Product not found at url: {command.arg['url']}")
                res = True
            except IndexError:
                print(f"Unsupported price model at url: {command.arg['url']}")
                res = True

            if not res:
                remaining_list.append(command)
        self.commands = remaining_list
