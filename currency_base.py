import time

class Usd_Currency:
    islem = 0
    usd_list = {}  # İşlem numarası -> tüm işlem detayları

    def __init__(self, rate, usd, transaction_firm, person):
        self.rate = rate
        self.usd = usd
        self.transaction_firm = transaction_firm
        self.person = person
        Usd_Currency.islem += 1

    def __str__(self):
        return f'{self.rate} TRY {self.usd} USD'

    def oran(self):
        total = self.rate * self.usd
        zaman = time.ctime()

        # İşlem numarasına göre tüm bilgiler saklanıyor
        Usd_Currency.usd_list[Usd_Currency.islem] = {
            "rate": self.rate,
            "usd": self.usd,
            "Total": total,
            "Transaction Firm": self.transaction_firm,
            "Person": self.person,
            "zaman": zaman
        }

        return f'{self.rate} TRY x {self.usd} USD = {total} TRY - İşlem Zamanı: {zaman}, Transaction Firm: {self.transaction_firm}, Person: {self.person}'

    @classmethod
    def transaction_list(cls):
        sonuc = ""
        for islem_no, detay in cls.usd_list.items():
            sonuc += (
                f"İşlem {islem_no}: Rate={detay['rate']}, USD={detay['usd']}, "
                f"Total={detay['Total']} TRY, Time={detay['zaman']}, "
                f"Transaction Firm={detay['Transaction Firm']}, Person={detay['Person']}\n"
            )
        return sonuc





# İşlemler
islem_1 = Usd_Currency(39, 500, 'upt', 'Test Name 1').oran()
islem_2 = Usd_Currency(39, 700, 'ria', 'Test Name 2').oran()
islem_3 = Usd_Currency(39, 800, 'ria', 'Test Name 3').oran()
islem_4 = Usd_Currency(39, 900, 'ria', 'Test Name 4').oran()
islem_5 = Usd_Currency(39, 1000, 'MoneyGram', 'Test Name 5').oran()

print(Usd_Currency.transaction_list())





