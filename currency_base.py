import time
from statistics import mean

class CurrencyBase:
    islem = 0

    def __init__(self, rate, amount, transaction_firm, person):
        self.rate = rate
        self.amount = amount
        self.transaction_firm = transaction_firm
        self.person = person
        CurrencyBase.islem += 1

    def __str__(self):
        return f'{self.rate} TRY x {self.amount}'

    def oran_alis(self):
        total = self.rate * self.amount
        zaman = time.ctime()

        self.__class__.currency_list[CurrencyBase.islem] = {
            "type": "alis",
            "rate": self.rate,
            "amount": self.amount,
            "Total": total,
            "Transaction Firm": self.transaction_firm,
            "Person": self.person,
            "zaman": zaman
        }

        return f'{self.rate} TRY x {self.amount} = {total} TRY - İşlem Zamanı: {zaman}, Transaction Firm: {self.transaction_firm}, Person: {self.person}'

    def oran_satis(self):
        total = self.rate * self.amount
        zaman = time.ctime()

        self.__class__.currency_list[CurrencyBase.islem] = {
            "type": "satis",
            "rate": self.rate,
            "amount": self.amount,
            "Total": total,
            "Transaction Firm": self.transaction_firm,
            "Person": self.person,
            "zaman": zaman
        }

        return f'{self.rate} TRY x {self.amount} = {total} TRY - İşlem Zamanı: {zaman}, Transaction Firm: {self.transaction_firm}, Person: {self.person}'

    @classmethod
    def transaction_list(cls):
        sonuc = ""
        for islem_no, detay in cls.currency_list.items():
            sonuc += (
                f"İşlem {islem_no}: Rate={detay['rate']}, Amount={detay['amount']}, "
                f"Total={detay['Total']} TRY, Time={detay['zaman']}, "
                f"Transaction Firm={detay['Transaction Firm']}, Person={detay['Person']}\n"
                f"Status = {detay['type']}\n"
            )
        return sonuc

    @classmethod
    def remove_transaction(cls, delete):
        try:
            delete = int(delete)
            if delete in cls.currency_list:
                cls.currency_list.pop(delete)
                print(f"İşlem {delete} Başarı ile Silindi")
            else:
                print("İşlem Numarası Bulunamadı")
        except ValueError:
            print("Geçersiz Numara")

    @classmethod
    def update_transaction(cls, islem_no, rate=None, amount=None, transaction_firm=None, person=None):
        try:
            islem_no = int(islem_no)
            if islem_no in cls.currency_list:
                cls.currency_list[islem_no]["rate"] = rate
                cls.currency_list[islem_no]["amount"] = amount
                cls.currency_list[islem_no]["Total"] = rate * amount
                cls.currency_list[islem_no]["Transaction Firm"] = transaction_firm
                cls.currency_list[islem_no]["Person"] = person

                return {islem_no: cls.currency_list[islem_no]}
        except ValueError:
            return "Lütfen geçerli bir işlem numarası giriniz"

    @classmethod
    def total_amount(cls):
        alis_try = []
        alis_amt = []
        satis_try = []
        satis_amt = []

        for islem_no, detay in cls.currency_list.items():
            if detay.get("type") == "alis":
                alis_try.append(detay["Total"])
                alis_amt.append(detay["amount"])
            elif detay.get("type") == "satis":
                satis_try.append(detay["Total"])
                satis_amt.append(detay["amount"])

        # Alış
        raw_alis_try = sum(alis_try)
        raw_alis_amt = sum(alis_amt)

        alis_toplam_try = f"{raw_alis_try:,.0f}".replace(",", ".") if alis_try else "0"
        alis_toplam_amt = f"{raw_alis_amt:,.0f}".replace(",", ".") if alis_amt else "0"
        alis_ortalama_kur = f"{(raw_alis_try / raw_alis_amt):,.2f}".replace(",", ".") if raw_alis_amt else "0.00"

        # Satış
        raw_satis_try = sum(satis_try)
        raw_satis_amt = sum(satis_amt)

        satis_toplam_try = f"{raw_satis_try:,.0f}".replace(",", ".") if satis_try else "0"
        satis_toplam_amt = f"{raw_satis_amt:,.0f}".replace(",", ".") if satis_amt else "0"
        satis_ortalama_kur = f"{(raw_satis_try / raw_satis_amt):,.2f}".replace(",", ".") if raw_satis_amt else "0.00"

        # Anlık TRY Durumu
        kasa_durumu = raw_alis_try - raw_satis_try
        if kasa_durumu == 0:
            durum_text = "✅ Kasa Durumu Dengede - İşleme Hazır"
        elif kasa_durumu > 0:
            durum_text = f" {-abs(kasa_durumu):,.2f}".replace(",", ".") + " TRY Kasa Eksiğiniz Mevcut"
        else:
            durum_text = f" {abs(kasa_durumu):,.2f}".replace(",", ".") + " TRY Kasa Fazlanız Mevcut"

        # Anlık Döviz Durumu
        doviz_kasa_durumu = raw_alis_amt - raw_satis_amt
        if doviz_kasa_durumu == 0:
            doviz_durum_text = "✅ Kasa Durumu Sıfır"
        elif doviz_kasa_durumu < 0:
            doviz_durum_text = f" {-abs(doviz_kasa_durumu):,.2f}".replace(",", ".") + " Döviz Eksiğiniz Mevcut"
        else:
            doviz_durum_text = f" {abs(doviz_kasa_durumu):,.2f}".replace(",", ".") + " Döviz Fazlanız Mevcut"

        return (
            f"\n🔹 Alış İşlemleri:\n"
            f"Toplam Miktar: {alis_toplam_amt}\n"
            f"Toplam TRY: {alis_toplam_try} TRY\n"
            f"Ortalama Kur: {alis_ortalama_kur} TRY"
            f"\n\n🔸 Satış İşlemleri:\n"
            f"Toplam Miktar: {satis_toplam_amt}\n"
            f"Toplam TRY: {satis_toplam_try} TRY\n"
            f"Ortalama Kur: {satis_ortalama_kur} TRY\n"
            f"\n🔹 Anlık Kasa Durumu:\n{durum_text}\n"
            f"\n🔹 Anlık Döviz Durumu:\n{doviz_durum_text}\n"
        )


class Usd_Currency(CurrencyBase):
    currency_list = {}
    def __init__(self, rate, usd, transaction_firm, person):
        super().__init__(rate, usd, transaction_firm, person)
        self.currency_type = "USD"

class Euro_Currency(CurrencyBase):
    currency_list = {}
    def __init__(self, rate, euro, transaction_firm, person):
        super().__init__(rate, euro, transaction_firm, person)
        self.currency_type = "EUR"




class Opening_Cash:

    cash = {}
    toplam = 0
    islem_no = 0

    def __init__(self, b200, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, fatura, other):
        self.b200 = b200
        self.b100 = b100
        self.b50 = b50
        self.b20 = b20
        self.b10 = b10
        self.b5 = b5
        self.payporter = payporter
        self.upt = upt
        self.moneygram = moneygram
        self.paragram = paragram
        self.fatura = fatura
        self.other = other
        self.zaman = time.ctime()

    def __str__(self):
        nakit_toplam = (
                self.b200 * 200 +
                self.b100 * 100 +
                self.b50 * 50 +
                self.b20 * 20 +
                self.b10 * 10 +
                self.b5 * 5
        )

        return (
            f"💵 Nakit Toplamı: {nakit_toplam:,.2f} TRY\n"
            f"• 200 TL x {self.b200}\n"
            f"• 100 TL x {self.b100}\n"
            f"• 50 TL x {self.b50}\n"
            f"• 20 TL x {self.b20}\n"
            f"• 10 TL x {self.b10}\n"
            f"• 5 TL x {self.b5}\n"
            f"\n📌 Diğer Bakiyeler:\n"
            f"Payporter: {self.payporter} TRY | UPT: {self.upt} TRY | MoneyGram: {self.moneygram} TRY | "
            f"Paragram: {self.paragram} TRY | Fatura: {self.fatura} TRY | Other: {self.other} TRY\n"
            f"🕒 İşlem Zamanı: {self.zaman}"
        )

    ### BU ALANDA BANKNOTLARI AYIRIYORUZ ###
    def toplam_nakit(self):
        toplam = (
                self.b200 * 200 +
                self.b100 * 100 +
                self.b50 * 50 +
                self.b20 * 20 +
                self.b10 * 10 +
                self.b5 * 5
        )
        return f"Toplam: {toplam:,.2f} TRY"

    def open_balance_try(self):
        Opening_Cash.islem_no += 1
        Opening_Cash.cash[Opening_Cash.islem_no] = {
            "nakit": self.toplam_nakit(),
            "payporter": self.payporter,
            "upt": self.upt,
            "moneygram": self.moneygram,
            "paragram": self.paragram,
            "fatura": self.fatura,
            "other": self.other,
            "zaman": self.zaman,
        }

    def open_balance_usd(self):
        Opening_Cash.islem_no += 1
        Opening_Cash.usd_cash[Opening_Cash.islem_no] = {
            "nakit": self.toplam_nakit(),
            "payporter": self.payporter,
            "upt": self.upt,
            "moneygram": self.moneygram,
            "paragram": self.paragram,
            "other": self.other,
            "zaman": self.zaman,
        }

    @classmethod
    def total_balance(cls):
        toplam = 0
        for no, kayit in Opening_Cash.cash.items():
            for key, value in kayit.items():
                if isinstance(value, (int, float)):
                    toplam += value
        return f"Toplam TRY Bakiyeniz -> {toplam} TRY"

    @classmethod
    def gunluk_bakiye_listesi(cls):
        for no, kayit in cls.cash.items():
            toplam = sum(value for value in kayit.values() if isinstance(value, (int, float)))
            zaman = kayit.get("zaman", "Bilinmiyor")
            print(f"İşlem No: {no} | Zaman: {zaman} | Toplam Bakiye: {toplam} TRY")


giris1 = Opening_Cash(1,1,1,1,0,0,100,1,1,1,1,1)
giris1.open_balance_try()

print(giris1.toplam_nakit())










# İşlemler
# alis_1 = Usd_Currency(39, 500, 'upt', 'Test Name 1').oran_alis()
# alis_2 = Usd_Currency(39, 700, 'ria', 'Test Name 2').oran_alis()
# alis_3 = Usd_Currency(39, 800, 'ria', 'Test Name 3').oran_alis()
# alis_4 = Usd_Currency(39, 900, 'ria', 'Test Name 4').oran_alis()
# alis_5 = Usd_Currency(39, 1000, 'MoneyGram', 'Test Name 5').oran_alis()
# alis_6 = Usd_Currency(40,852,"KoronaPay","Test Name 6")
# alis_6.oran_alis()
# satis_1 = Usd_Currency(40,1000,"Kişisel","Test Name 1").oran_satis()
# alis_7 = CurrencyBase(30,1000,"upt",'Test Name 7').oran_alis()

# print(Usd_Currency.transaction_list())
# Usd_Currency.remove_transaction(1)
# Usd_Currency.remove_transaction(2)
# print(Usd_Currency.transaction_list())

# CurrencyBase.update_transaction(4,45,250,"IntelExpress","Test Name 4")

