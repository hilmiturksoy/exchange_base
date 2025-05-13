import time
from os import remove


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

    @classmethod
    def remove_transaction(cls, delete):
        try:
            delete = int(delete)
            if delete in cls.usd_list:
                cls.usd_list.pop(delete)
                print(f"İşlem {delete} Başarı ile Silindi")
            else:
                print("İşlem Numarası Bulunamadı")

        except ValueError:
            print("Geçersiz Numara")

    @classmethod
    def update_transaction(cls, islem_no, rate=None, usd=None, transaction_firm=None, person=None):
        try:
            islem_no = int(islem_no)
            if islem_no in cls.usd_list:
                cls.usd_list[islem_no]["rate"] = rate
                cls.usd_list[islem_no]["usd"] = usd
                cls.usd_list[islem_no]["Total"] = rate * usd
                cls.usd_list[islem_no]["Transaction Firm"] = transaction_firm
                cls.usd_list[islem_no]["Person"] = person


                return {islem_no: cls.usd_list[islem_no]}
        except ValueError:
            return "Lütfen geçerli bir işlem numarası giriniz"

    @classmethod
    def total_amount(cls):
        toplam_try = []
        toplam_usd = []

        print("🔹 TRY Bazlı İşlemler:")
        for islem_no, detay in cls.usd_list.items():
            formatted_try = f"{detay['Total']:,.0f}".replace(",", ".")
            print(f"İşlem {islem_no}: {formatted_try} TRY")
            toplam_try.append(detay['Total'])

        print("\n🔹 USD Bazlı İşlemler:")
        for islem_no, detay in cls.usd_list.items():
            formatted_usd = f"{detay['usd']:,.0f}".replace(",", ".")
            print(f"İşlem {islem_no}: {formatted_usd} USD")
            toplam_usd.append(detay['usd'])  # str değil, float ekliyoruz

        genel_toplam_try = f"{sum(toplam_try):,.0f}".replace(",", ".")
        genel_toplam_usd = f"{sum(toplam_usd):,.0f}".replace(",", ".")

        return f"\n Genel Toplamlar:\nUSD: {genel_toplam_usd} USD\nTRY: {genel_toplam_try} TRY"

        genel_toplam_try = f"{sum(toplam_try):,.0f}".replace(",", ".")
        return f"\nGenel Toplam: {genel_toplam_try} TRY"

        genel_toplam_usd = f"{sum(toplam_usd):,.0f}".replace(",", ".")
        return f"\nGenel Toplam: {genel_toplam_usd} USD"


# İşlemler
islem_1 = Usd_Currency(39, 500, 'upt', 'Test Name 1').oran()
islem_2 = Usd_Currency(39, 700, 'ria', 'Test Name 2').oran()
islem_3 = Usd_Currency(39, 800, 'ria', 'Test Name 3').oran()
islem_4 = Usd_Currency(39, 900, 'ria', 'Test Name 4').oran()
islem_5 = Usd_Currency(39, 1000, 'MoneyGram', 'Test Name 5').oran()
islem_6 = Usd_Currency(40,852,"KoronaPay","Test Name 6").oran()

# print(Usd_Currency.transaction_list())
# Usd_Currency.remove_transaction(1)
# Usd_Currency.remove_transaction(2)
# print(Usd_Currency.transaction_list())

Usd_Currency.update_transaction(4,45,250,"IntelExpress","Test Name 4")
print(Usd_Currency.transaction_list())

print(Usd_Currency.total_amount())