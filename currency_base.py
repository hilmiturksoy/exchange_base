import time
from os import remove
from statistics import mean



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

    def oran_alis(self):
        total = self.rate * self.usd
        zaman = time.ctime()

        Usd_Currency.usd_list[Usd_Currency.islem] = {
            "type": "alis",
            "rate": self.rate,
            "usd": self.usd,
            "Total": total,
            "Transaction Firm": self.transaction_firm,
            "Person": self.person,
            "zaman": zaman
        }

        return f'{self.rate} TRY x {self.usd} USD = {total} TRY - İşlem Zamanı: {zaman}, Transaction Firm: {self.transaction_firm}, Person: {self.person}'

    def oran_satis(self):
        total = self.rate * self.usd
        zaman = time.ctime()

        Usd_Currency.usd_list[Usd_Currency.islem] = {
            "type": "satis",
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
                f"Status = {detay['type']}\n"
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

    from statistics import mean  # En üstte olmalı

    @classmethod
    def total_amount(cls):
        alis_try = []
        alis_usd = []
        satis_try = []
        satis_usd = []

        for islem_no, detay in cls.usd_list.items():
            if detay.get("type") == "alis":
                alis_try.append(detay["Total"])
                alis_usd.append(detay["usd"])
            elif detay.get("type") == "satis":
                satis_try.append(detay["Total"])
                satis_usd.append(detay["usd"])

        # Alış
        raw_alis_try = sum(alis_try)
        raw_alis_usd = sum(alis_usd)

        alis_toplam_try = f"{raw_alis_try:,.0f}".replace(",", ".") if alis_try else "0"
        alis_toplam_usd = f"{raw_alis_usd:,.0f}".replace(",", ".") if alis_usd else "0"
        alis_ortalama_kur = f"{(raw_alis_try / raw_alis_usd):,.2f}".replace(",", ".") if raw_alis_usd else "0.00"


        # Satış
        raw_satis_try = sum(satis_try)
        raw_satis_usd = sum(satis_usd)

        satis_toplam_try = f"{sum(satis_try):,.0f}".replace(",", ".") if satis_try else "0"
        satis_toplam_usd = f"{sum(satis_usd):,.0f}".replace(",", ".") if satis_usd else "0"
        satis_ortalama_usd = f"{(raw_satis_try / raw_satis_usd):,.2f}".replace(",", ".") if raw_satis_usd else "0.00"

        # Anlik TRY Durumu
        kasa_durumu = raw_alis_try - raw_satis_try  # float olarak hesapla
        status_try = f"{kasa_durumu:,.2f}".replace(",", ".")  # sadece yazdırmak için string'e çevir

        if kasa_durumu == 0:
            durum_text = "✅ Kasa Durumu Dengede - İşleme Hazır"
        elif kasa_durumu > 0:
            durum_text = f" {-abs(kasa_durumu):,.2f}".replace(",", ".") + " TRY Kasa Eksiğiniz Mevcut"

        else:
            durum_text = f" {abs(kasa_durumu):,.2f}".replace(",", ".") + " TRY Kasa Fazlanız Mevcut"


        return (
            f"\n🔹 Alış İşlemleri:\n"
            f"Toplam USD: {alis_toplam_usd} USD\n"
            f"Toplam TRY: {alis_toplam_try} TRY\n"
            f"Ortalama USD: {alis_ortalama_kur} USD"

            f"\n\n🔸 Satış İşlemleri:\n"
            f"Toplam USD: {satis_toplam_usd} USD\n"
            f"Toplam TRY: {satis_toplam_try} TRY\n"
            f"Ortalama USD: {satis_ortalama_usd} USD\n"
            
            f"\n🔹 Anlık Kasa Durumu:\n"
            f" TRY: {durum_text} TRY\n"
        )


# İşlemler
# alis_1 = Usd_Currency(39, 500, 'upt', 'Test Name 1').oran_alis()
# alis_2 = Usd_Currency(39, 700, 'ria', 'Test Name 2').oran_alis()
# alis_3 = Usd_Currency(39, 800, 'ria', 'Test Name 3').oran_alis()
# alis_4 = Usd_Currency(39, 900, 'ria', 'Test Name 4').oran_alis()
# alis_5 = Usd_Currency(39, 1000, 'MoneyGram', 'Test Name 5').oran_alis()
# alis_6 = Usd_Currency(40,852,"KoronaPay","Test Name 6").oran_alis()
# satis_1 = Usd_Currency(40,1000,"Kişisel","Test Name 1").oran_satis()
alis_7 = Usd_Currency(30,1000,"upt",'Test Name 7').oran_alis()

# print(Usd_Currency.transaction_list())
# Usd_Currency.remove_transaction(1)
# Usd_Currency.remove_transaction(2)
# print(Usd_Currency.transaction_list())

Usd_Currency.update_transaction(4,45,250,"IntelExpress","Test Name 4")

print(Usd_Currency.total_amount())




