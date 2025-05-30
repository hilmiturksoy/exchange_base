import time
from functools import total_ordering
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
        total = float(self.rate * self.amount)
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

    """
    RAW_ALIS_TRY --->ANA TRY KASASINDAN CIKIS YAPILIR
    RAW_SATIS_TRY --->ANA TRY KASASINA GIRIS YAPILIR
    RAW_SATIS_AMT --->ANA DOVIZ KASASINDAN CIKIS YAPILIR
    RAW_ALIS_AMT ---> ANA DOVIZ KASASINA GIRIS YAPILIR
    BU ALAN TOTAL_AMOUNT SINIFINDAN KOPYALANMIŞTIR
    """

    @property
    def sum_for_total_amount(self):
        alis_try = []
        alis_amt = []
        satis_try = []
        satis_amt = []

        for islem_no, detay in self.__class__.currency_list.items():
            if detay.get("type") == "alis":
                alis_try.append(detay["Total"])
                alis_amt.append(detay["amount"])
            elif detay.get("type") == "satis":
                satis_try.append(detay["Total"])
                satis_amt.append(detay["amount"])

        raw_alis_try = sum(alis_try)
        raw_alis_amt = sum(alis_amt)
        raw_satis_try = sum(satis_try)
        raw_satis_amt = sum(satis_amt)

        return raw_alis_try, raw_alis_amt, raw_satis_try, raw_satis_amt


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
    """
    BU ALANDA GUNLUK KASA ACILISI YAPILMAKTADIR
    PARA BIRIMLERININ GIRISLERI YAPILIR VE KASAYA ACILIS ICIN EKLENIR (SELF.CASH)
    """
    def __init__(self, b200=0, b100=0, b50=0, b20=0, b10=0, b5=0,
                 payporter=0, upt=0, moneygram=0, paragram=0, other=0):
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
        self.other = other
        self.zaman = time.ctime()

        self.islem_no = 0
        self.cash = {}

    def toplam_nakit_sayi(self):
        return (
            self.b200 * 200 +
            self.b100 * 100 +
            self.b50 * 50 +
            self.b20 * 20 +
            self.b10 * 10 +
            self.b5 * 5
        )

    def open_balance(self):
        self.islem_no += 1
        self.cash[self.islem_no] = {
            "nakit": self.toplam_nakit_sayi(),
            "payporter": self.payporter,
            "upt": self.upt,
            "moneygram": self.moneygram,
            "paragram": self.paragram,
            "other": self.other,
            "zaman": self.zaman,
        }

    @property
    def total_balance(self):
        toplam = 0
        for no, kayit in self.cash.items():
            for key, value in kayit.items():
                if isinstance(value, (int, float)):
                    toplam += value
        return toplam




    def gunluk_bakiye_listesi(self):
        sonuc = []
        for no, kayit in self.cash.items():
            toplam = sum(value for value in kayit.values() if isinstance(value, (int, float)))
            zaman = kayit.get("zaman", "Bilinmiyor")
            sonuc.append(f"İşlem No: {no} | Zaman: {zaman} | Toplam Bakiye: {toplam} ")
        return "\n".join(sonuc)

    @property
    def nakit_kasa(self):
        toplam = 0
        for kayit in self.cash.values():
            if 'nakit' in kayit and isinstance(kayit['nakit'], (int, float)):
                toplam += kayit['nakit']
        return toplam

    def guncel_nakit_durum(self, currency_class):
        """
        currency_class: Usd_Currency gibi CurrencyBase'den türeyen sınıf
        """
        if not hasattr(currency_class, "sum_for_total_amount"):
            raise ValueError("Geçersiz döviz sınıfı")

        try:
            raw_alis_try, _, raw_satis_try, _ = currency_class.sum_for_total_amount()
            return self.nakit_kasa + raw_satis_try - raw_alis_try
        except Exception as e:
            print(f"Hata: {e}")
            return self.nakit_kasa



class Try_Opening_Cash(Opening_Cash):
    def __init__(self, b200, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, other):
        super().__init__(b200, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, other)
        self.kasa_turu = "TRY"

    def update_with_transaction_result(self, raw_alis_try, raw_satis_try):
        fark = raw_satis_try - raw_alis_try
        if self.islem_no in self.cash:
            self.cash[self.islem_no]["try_hareket"] = fark
            self.cash[self.islem_no]["nakit"] += fark
        else:
            print("🔴 Uyarı: İlgili işlem numarası bulunamadı.")

        return fark

    def kasa_bilgisi(self):
        return f"Kasa Türü: {self.kasa_turu} | {self.total_balance}"




class Usd_Opening_Cash(Opening_Cash):
    def __init__(self, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, other):
        super().__init__(0, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, other)
        self.kasa_turu = "USD"  # örnek ek alan

    def kasa_bilgisi(self):
        return f"Kasa Türü: {self.kasa_turu} | {self.total_balance}"


class Euro_Opening_Cash(Opening_Cash):
    def __init__(self, b200, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, other):
        super().__init__(b200, b100, b50, b20, b10, b5, payporter, upt, moneygram, paragram, other)
        self.kasa_turu = "EURO"  # örnek ek alan

    def kasa_bilgisi(self):
        return f"Kasa Türü: {self.kasa_turu} | {self.total_balance}"




"""genel kasa girisi"""
kasa_acilis = Try_Opening_Cash(1,1,0,0,0,0,0,0,0,0,0)
kasa_acilis.open_balance()
print(kasa_acilis.kasa_bilgisi())


usd_alis = Usd_Currency(40,100,"ria","test")
usd_alis.oran_alis()
usd_satis = Usd_Currency(45,100,"ria", "test")
usd_satis.oran_satis()

print(f"Sonuc {usd_alis.sum_for_total_amount}")

print(f" kasa acilis {kasa_acilis.nakit_kasa}")
# print(type(kasa_acilis.nakit_kasa))


def guncel_nakit_durum():
    resould = kasa_acilis.nakit_kasa + usd_alis.sum_for_total_amount[0] - usd_alis.sum_for_total_amount[2]
    return resould

print(guncel_nakit_durum())
