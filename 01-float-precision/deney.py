import numpy as np

def naif_toplam(x):
    toplam = x.dtype.type(0)
    for v in x:
        toplam = toplam + v
    return toplam


rng = np.random.default_rng(42)

for n in [10**3, 10**4, 10**5, 10**6, 10**7, 10**8]:
    x = rng.random(n)
    toplam64 = x.astype(np.float64).sum()
    toplam32 = x.astype(np.float32).sum()
    mutlak_fark = abs(toplam64 - toplam32)
    goreli = mutlak_fark / abs(toplam64)
    print(f"n: {n}, toplam={toplam64} mutlak fark={mutlak_fark} göreli={goreli}")

    naif_toplam_ = naif_toplam(x.astype(np.float32))
    naif_goreli = abs(toplam64 - naif_toplam_) / abs(toplam64)
    print(f"Naif Toplam: {naif_toplam_}")
    print(f"Naif Göreli: {naif_goreli}")
    



# Deneme deneyi
a = np.float32(2**24)
print(a + np.float32(1) == a)

# Sınır Testleri
print(a + np.float32(1) == a) #aynı
print(a + np.float32(2) == a) # Farklı çıktı, sınırın üstü
print(np.float32(2**25) + np.float32(2)) 

# Beraber
for k in [10, 20, 23, 24, 25, 30]:
    print(k, np.spacing(np.float32(2**k)))