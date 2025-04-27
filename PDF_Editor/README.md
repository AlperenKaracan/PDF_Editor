# PDF Düzenleyici

## Özellikler
* **PDF Birleştir (Sıralı Seçim):** `pdfs` klasöründeki birden fazla PDF dosyasını, kullanıcı tarafından belirtilen sırayla tek bir PDF'te birleştirir.
* **PDF Böl (Sayfa Seçimi):** `pdfs` klasöründeki bir PDF dosyasından belirli sayfaları veya sayfa aralıklarını ayıklar ve bunları yeni bir PDF olarak kaydeder.
* **PDF Döndür:** Bir PDF'in seçili sayfalarını veya tüm sayfalarını 90, 180 veya 270 derece saat yönünde veya saat yönünün tersine döndürür.
* **Görsellerden PDF Oluştur:** `images` klasöründeki PNG, JPG veya JPEG formatındaki resimleri, kullanıcı tarafından tanımlanan sırayla tek bir PDF dosyasına dönüştürür.

## Gereksinimler
* Python 3
* PyPDF2 (`pip install pypdf2`)
* Pillow (`pip install Pillow`)

## Kurulum
1. Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install pypdf2 Pillow
    ```
2. pdfci.py ile  aynı dizinde aşağıdaki alt dizinleri oluşturun:
    * `pdfs`: İşlemek istediğiniz PDF dosyalarını buraya yerleştirin.
    * `images`: Dönüştürmek istediğiniz resim dosyalarını (PNG, JPG, JPEG) buraya yerleştirin.
    * `output`: İşlenen dosyalar buraya kaydedilecektir.

## Kullanım
Terminalinizden çalıştırın:
```bash
python pdfci.py