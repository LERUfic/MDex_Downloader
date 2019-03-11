# MDex_Downloader
MangaDex Downloader using Python3. Hanya sebuah script sebagai bentuk riset penggunaan selenium sebagai drivernya namun ~~crawling~~ scrapingnya menggunakan beautifulsoup.

Ini chromedrivernya mac. Jadi bisa download di http://chromedriver.chromium.org/ sesuai dengan OS masing-masing. 


Known Issues:
 - ~~Download lambat karena waktu tunggu halaman 3 detik setiap gambar~~
 - Tidak ada error handling ketika koneksi terputus (no resume download)
 - MD loadingnya lambat membuat tidak dapat image link

To Do:
- [x] Error handling ketika tidak dapat image link. (Butuh test lebih banyak)
- [ ] Optimasi download dengan thread
- [x] Mengefisienkan alur program sehingga tidak ada kegiatan yang redundant
- [ ] Error handling ketika koneksi terputus

Changelog:
- 3/12/2019 05:58:
   - Benerin beberapa error
- 3/11/2019 17:37:
   - Flow yang lebih baik
   - Memperbaiki error ketika manga link diakhiri dengan slash
- 3/10/2019 23:40:
   - Menghapus penggunaan time.sleep karena setiap halaman memiliki besar assets yang berbeda
   - Timeout diperbesar jadi 1 menit yang semula ketika menggunakan time.sleep adalah 3 detik