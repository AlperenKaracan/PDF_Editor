import os
from datetime import datetime
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, 'pdfs')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')
IMAGE_FOLDER = os.path.join(BASE_DIR, 'images')

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def list_pdfs(folder):
    pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    pdf_info = []
    for pdf in pdf_files:
        try:
            reader = PdfReader(os.path.join(folder, pdf))
            total_pages = len(reader.pages)
            pdf_info.append((pdf, total_pages))
        except Exception:
            pdf_info.append((pdf, '💥 Hata!'))
    return pdf_info

def list_images(folder):
    return [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

def parse_page_ranges(input_string):
    pages = set()
    parts = input_string.split(',')
    for part in parts:
        if '-' in part:
            start, end = part.split('-')
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(part))
    return sorted(pages)

def get_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M')

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    total_pages = 0
    for pdf in pdf_list:
        merger.append(pdf)
        reader = PdfReader(pdf)
        pdf_page_count = len(reader.pages)
        total_pages += pdf_page_count
        print(f'🚀 "{os.path.basename(pdf)}" dosyasını trene bindirdik ({pdf_page_count} sayfa)')
    merger.write(output_path)
    merger.close()
    print(f'🎉 Şefim birleştirme tamamdır,Final dosya: {output_path} (Toplam {total_pages} sayfa)')

def split_pdf(pdf_path, output_folder, page_ranges):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f'📄 PDF toplam {total_pages} sayfa içeriyor.')

    selected_pages = [p for p in page_ranges if 1 <= p <= total_pages]
    if not selected_pages:
        print('😅 Geçerli bir sayfa seçmedin.')
        return

    writer = PdfWriter()
    for page_num in selected_pages:
        writer.add_page(reader.pages[page_num - 1])
        print(f'✂️ Sayfa {page_num} parçalandı,dosyaya eklendi.')

    timestamp = get_timestamp()
    output_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(pdf_path))[0]}_selected_pages_{timestamp}.pdf')
    with open(output_filename, 'wb') as output_pdf:
        writer.write(output_pdf)

    print(f'🎯 Operasyon başarıyla tamamlandı, Çıktı dosyası: {output_filename}')

def rotate_selected_pages(pdf_path, output_folder, rotation_angle, page_ranges, direction, rotate_all=False):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)
    print(f'📄 PDF toplam {total_pages} sayfa içeriyor.')

    if rotate_all:
        selected_pages = range(1, total_pages + 1)
    else:
        selected_pages = [p for p in page_ranges if 1 <= p <= total_pages]

    if not selected_pages:
        print('😅 Patron sayfa seçmedin ki döndürelim')
        return

    for page_num, page in enumerate(reader.pages, start=1):
        if page_num in selected_pages:
            if direction == 'c':
                page.rotate(rotation_angle)
                print(f'🔄 Sayfa {page_num} {rotation_angle} derece saat yönünde döndürüldü.')
            else:
                page.rotate(-rotation_angle)
                print(f'🔄 Sayfa {page_num} {rotation_angle} derece saat yönünün tersine döndürüldü.')
        else:
            print(f'➡️ Sayfa {page_num} olduğu gibi kaldı,dokunmadık.')
        writer.add_page(page)

    timestamp = get_timestamp()
    output_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(pdf_path))[0]}_rotated_selected_{rotation_angle}_{direction}_{timestamp}.pdf')
    with open(output_filename, 'wb') as output_pdf:
        writer.write(output_pdf)

    print(f'🎯 Patron döndürme operasyonu tamamlandı,Çıktı dosyası: {output_filename}')

def images_to_pdf(image_folder, output_folder):
    images = list_images(image_folder)
    if not images:
        print('🚫 Şefim klasörde görsel yok,önce malzeme lazım.')
        return

    print('🖼️ Elimizdeki görseller:')
    for idx, img in enumerate(images):
        print(f'  {idx + 1}. {img}')

    sequence = input('PDF oluşturma sırasını yaz bakalım (örn: 3,2,1): ')
    try:
        order = [int(num.strip()) - 1 for num in sequence.split(',')]
        ordered_images = [os.path.join(image_folder, images[i]) for i in order if 0 <= i < len(images)]
        if not ordered_images:
            print('🚫 Şefim geçerli sıra vermedin, müşteri bekliyor')
            return

        image_objs = []
        for img_path in ordered_images:
            img = Image.open(img_path).convert('RGB')
            image_objs.append(img)
            print(f'🖼️ "{os.path.basename(img_path)}" resmi eklendi.')

        timestamp = get_timestamp()
        output_filename = os.path.join(output_folder, f'gorsellerden_pdf_{timestamp}.pdf')
        image_objs[0].save(output_filename, save_all=True, append_images=image_objs[1:])
        print(f'🎯 Şefim görseller PDF oldu,Çıktı dosyası: {output_filename}')

    except Exception as e:
        print(f'💥 Görsellerden PDF yaparken patladık: {e}')

def main():
    print("""
    ===========================
    1. PDF Birleştir (Sıralı Seçim)
    2. PDF Böl (Sayfa Seçimi)
    3. PDF Döndür (Seçilen Sayfalar veya Tamamını Döndür)
    4. Görsellerden PDF Oluştur
    ===========================
    """)
    choice = input('Hangisini yapmak istiyorsun patron? (1, 2, 3 veya 4): ')
    if choice == '1':
        pdfs = list_pdfs(PDF_FOLDER)
        if not pdfs:
            print('🚫 Şefim klasörde PDF yok,önce malzeme lazım.')
            return

        print('📂 Elimizdeki PDF stokları:')
        for idx, (pdf, total_pages) in enumerate(pdfs):
            print(f'  {idx + 1}. {pdf} ({total_pages} sayfa)')

        sequence = input('Birleştirme sırasını yaz bakalım (örn: 3,2,1): ')
        try:
            order = [int(num.strip()) - 1 for num in sequence.split(',')]
            ordered_pdfs = [os.path.join(PDF_FOLDER, pdfs[i][0]) for i in order if 0 <= i < len(pdfs)]
            if not ordered_pdfs:
                print('🚫 Şefim geçerli sıra vermedin,müşteri bekliyor')
                return

            timestamp = get_timestamp()
            output = os.path.join(OUTPUT_FOLDER, f'birlesik_sirali_{timestamp}.pdf')
            merge_pdfs(ordered_pdfs, output)
        except Exception as e:
            print(f'💥 Eyvah! Bir şeyler patladı: {e}')

    elif choice == '2':
        pdfs = list_pdfs(PDF_FOLDER)
        if not pdfs:
            print('🚫 Şefim klasörde PDF yok, önce malzeme lazım.')
            return

        print('📂 Elimizdeki PDF stokları:')
        for idx, (pdf, total_pages) in enumerate(pdfs):
            print(f'  {idx + 1}. {pdf} ({total_pages} sayfa)')

        selected = int(input('Bölmek istediğin PDF numarasını yaz şefim: ')) - 1
        if 0 <= selected < len(pdfs):
            page_input = input('Hangi sayfaları istiyorsun? (örn: 1-3,5,7): ')
            try:
                page_ranges = parse_page_ranges(page_input)
                split_pdf(os.path.join(PDF_FOLDER, pdfs[selected][0]), OUTPUT_FOLDER, page_ranges)
            except Exception as e:
                print(f'💥 Sayfa seçimi patladı şefim: {e}')
        else:
            print('🚫 Şefim yanlış seçim yaptın, müşteri bekliyor.')

    elif choice == '3':
        pdfs = list_pdfs(PDF_FOLDER)
        if not pdfs:
            print('🚫 Şefim klasörde PDF yok, önce malzeme lazım.')
            return

        print('📂 Elimizdeki PDF stokları:')
        for idx, (pdf, total_pages) in enumerate(pdfs):
            print(f'  {idx + 1}. {pdf} ({total_pages} sayfa)')

        selected = int(input('Döndürmek istediğin PDF numarasını yaz şefim: ')) - 1
        if 0 <= selected < len(pdfs):
            angle = int(input('Kaç derece döndürelim? (90, 180, 270): '))
            if angle not in [90, 180, 270]:
                print('🚫 Şefim sadece 90, 180 veya 270 derece döndürebiliyoruz.')
                return

            page_input = input('Hangi sayfaları döndürmek istiyorsun? (örn: 1-3,5,7 ya da tüm sayfalar için "all" veya "tamamı"): ')
            direction_input = input('Yönü seç şefim: Saat yönü için "c", ters için "cc": ').strip().lower()
            if direction_input not in ['c', 'cc']:
                print('🚫 Şefim yönü yanlış girdin, sadece "c" veya "cc" olmalı.')
                return
            try:
                if page_input.lower() in ['all', 'tamamı']:
                    rotate_all = True
                    page_ranges = []
                else:
                    rotate_all = False
                    page_ranges = parse_page_ranges(page_input)
                rotate_selected_pages(os.path.join(PDF_FOLDER, pdfs[selected][0]), OUTPUT_FOLDER, angle, page_ranges, direction_input, rotate_all)
            except Exception as e:
                print(f'💥 Döndürme işlemi patladı şefim: {e}')
        else:
            print('🚫 Şefim yanlış seçim yaptın, müşteri bekliyor.')

    elif choice == '4':
        images_to_pdf(IMAGE_FOLDER, OUTPUT_FOLDER)

    else:
        print('🚫 Şefim öyle bir seçenek yok.')

if __name__ == '__main__':
    main()
