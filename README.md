# 🎙️ Arapça Telaffuz ve Konuşma Asistanı — Muallimun.Net (v31)

**Arapça Telaffuz ve Konuşma Asistanı**, Arapça öğrenen öğrencilerin kelime hazinesini, anahtar cümle kalıplarını ve karşılıklı diyalog (المحادثة والتكلم) becerilerini geliştirmek amacıyla **Muallimun.Net** tarafından geliştirilmiş, yapay zeka destekli interaktif bir dil laboratuvarıdır.

---

## ✨ Temel Özellikler

* **🏠 Kelime Modu (`data/kelimeler.db`):**
  * Paket/kategori bazlı çalışma, görseli olmayan kelimeler için otomatik ortalanmış büyük tipografi (`Arakom.ttf`).
  * **🇹🇷 Türkçe Göster/Gizle** ve **Hareke Göster/Gizle** seçenekleriyle öz-değerlendirme.
  * **⭐ Tekrar Listem** ve **🎯 Zayıflar** özel çalışma listeleri.
* **💬 Diyalog Modu (`data/diyaloglar.db`):**
  * **📖 Öğrenme Modu:** Diyaloğun tamamını veya tekil cümleleri sesli dinleme, okunan cümleyi otomatik vurgulama ve ekranda otomatik kaydırma.
  * **🎭 Ölçme / Canlandırma (Rol Yapma) Modu:** Diyalogdaki bir karakterin rolünü üstlenerek uygulamayla karşılıklı konuşma. Doğru söylenen kelimelerin **Yeşil**, eksik/hatalı kelimelerin **Kırmızı** renkte açılması ve oturum sonunda **📊 Konuşma Karnesi**.
  * **✏️ Tekil Cümle Düzenleme:** Her konuşma balonunun üzerinden ilgili cümleyi anında düzenleme.
* **📜 Cümle Modu (`data/cumleler.db`):**
  * 7.950+ anahtar cümle, **🙈 Arapçayı Gizle (Ölçme)** modu, Favoriler ve Öğrendiklerim filtreleri.
* **🛠️ Birleşik Yönetim & Paket Paneli (Admin):**
  * Binlerce kayıt arasında anında arama, diyalog filtreleme ve sayfalama.
  * Görsel (`images/`) ve ses (`sounds/`) dosyalarıyla birlikte **Tam Medyalı `.ZIP` Paket İçe/Dışa Aktarma**.
  * Yerel dosya veya internet bağlantısı (**🌐 URL İndir**) ile özel ses eşleştirme.
  * **⚡ Çevrimdışı TTS Hazırlayıcı** ve **🪄 Veritabanı Metin Doktoru**.
* **📊 Raporlar, Rozetler ve Günlük Seri (Streak):**
  * Öğrenci motivasyonu için **🔥 Günlük Seri (Streak)**, seviye sistemi ve başarı rozetleri.
  * Öğretmenler için paket/diyalog tamamlama grafikleri, en çok hata yapılan ifadeler listesi ve **Excel (CSV) Rapor Çıktısı**.
* **🎨 Aydınlık ve Karanlık Tema:** Akıllı tahtalar için yüksek kontrastlı Aydınlık Mod ve bireysel çalışma için Karanlık Mod.

---

## 🚀 Kurulum ve Çalıştırma

1. **Python 3.10+** kurulu olduğundan emin olun.
2. Proje klasöründe sanal ortam oluşturun ve bağımlılıkları yükleyin:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt