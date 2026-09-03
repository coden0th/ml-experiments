import numpy as np
import math

rng = np.random.default_rng(42)

def naif_toplam(x):
    toplam = x.dtype.type(0)
    for v in x:
        toplam = toplam + v
    return toplam

orjinal = rng.random(10**6)
toplam_listesi = []
# print(f"Orjinal: {orjinal}")
for n in range(100):
    kopya_dizi = rng.permutation(orjinal)
    toplam = naif_toplam(kopya_dizi)
    toplam_listesi.append(toplam)

    # print(f"Karıştırılmış Dizi {n+1}: {kopya_dizi}")
    # print(f"Toplam: {toplam}")


# print(f"Toplamlar: {toplam_listesi}")
max_toplam = max(toplam_listesi)
min_toplam = min(toplam_listesi)
karsilastirma = max_toplam - min_toplam
print(f"Max-Min Fark: {karsilastirma}")

kopya_dize = orjinal.copy()
sortlanmis = naif_toplam(np.sort(kopya_dize))
print(f"Toplam: {sortlanmis}")
en_buyuk_sortlanmis = naif_toplam(np.sort(kopya_dize)[::-1])
print(f"Toplam: {en_buyuk_sortlanmis}")

orjinalsum = math.fsum(orjinal)
print(f"Doğru Toplam: {orjinalsum}")
print(f"Sorlanmis ne kadar uzak: {abs(sortlanmis - orjinalsum)}")
print(f"En Büyük Sıralanmış ne kadar uzak: {abs(en_buyuk_sortlanmis - orjinalsum)}")
print(f"Permütasyondaki en büyük: {abs(max_toplam - orjinalsum)}")
print(f"Permütasyondaki en küçük: {abs(min_toplam - orjinalsum)}")