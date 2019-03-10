# MDex_Downloader
MangaDex Downloader using Python3. Hanya sebuah script sebagai bentuk riset penggunaan selenium sebagai drivernya namun scrapingnya menggunakan beautifulsoup.

Known Issues:
 - Download lambat karena waktu tunggu halaman 3 detik setiap gambar
 - MD loadingnya lambat membuat tidak dapat image link

To Do:
- [x] Error handling ketika tidak dapat image link. (Butuh test lebih banyak)
- [ ] Optimasi download dengan thread
- [ ] Mengefisienkan alur program sehingga tidak ada kegiatan yang redundant