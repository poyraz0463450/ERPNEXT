# Geri Yukleme

Bu yedek, ERPNext ortamini tekrar kurmak ve ARTEGON ozel gelistirmelerini geri almak icin hazirlandi.

Adimlar:
1. Frappe Bench ve ERPNext `develop` surumlerini kur.
2. `artegon_otomasyon/` klasorunu bench altindaki `apps/` dizinine kopyala.
3. `bench_meta/apps.txt` ve `bench_meta/apps.json` dosyalarini referans alarak uygulama listesini dogrula.
4. Site olustururken `bench_meta/site_config.example.json` icindeki alanlari kendi veritabani bilgilerinle doldur.
5. `artegon_otomasyon` uygulamasini siteye yukle:

```bash
bench --site erpnext.localhost install-app artegon_otomasyon
```

6. Demo veri ve is akislarini tekrar yuklemek icin uygulama icindeki kurulum betiklerini kullan:

```bash
bench --site erpnext.localhost execute artegon_otomasyon.demo_setup.run
bench --site erpnext.localhost execute artegon_otomasyon.ui_setup.apply_simplified_ui
```

7. `demo_teknik_resimler/` altindaki PDF dosyalarini tekrar dosya alanina yukleyebilirsin.
8. Referans ekran tasarimi ve akislari icin `reference_erp_ui/` klasorunu kullan.

Not:
- Bu repoda canli veritabani dump'i yoktur.
- Bu repoda canli site sifreleri yoktur.
- Tam birebir canli ortam kopyasi istenirse o islem private repo veya sifreli arsiv ile yapilmalidir.
