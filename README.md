Kodlayalım
===========

## Proje Konusu

Temel programlama eğitimi

## Giriş Bilgileri

| Rol      | E-posta          | Parola |
| -------- | ---------------- | ------ |
| Eğitimci | teacher@acme.com | 123456 |
| Öğrenci  | student@acme.com | 123456 |

## Rollere göre yetenekler

### Eğitimci

- Ders oluşurabilir
- Dersi güncelleyebilir

> Ders oluşturabilmek için sağ üst köşede bulunan menüden Derslerim bağlantısına tıklamanız gerekmektedir.


### Öğrenci

- Sistemdeki dersleri görüntüleyebilir
- Ders içeriklerine erişebilir


### Tüm Kullanıcı Rolleri

- Tüm dersleri görüntüleyebilir
- Profil sayfasını düzenleyebilir

## Kurulum

```bash
pip3 install -r requirements.txt

export FLASK_APP=./kodlayalim_app.py
export FLASK_DEBUG=True

flask run
```

[http://127.0.0.1:5000](http://127.0.0.1:5000) adresini ziyaret edebilirsiniz.

### Not:

- `direnv` paketini sisteme kurmanız halinde çevre değişkenleri her seferinde export etmenize gerek kalmaz. Bu değişkenleri .envrc dosyasından yönetebilirsiniz.

> https://github.com/direnv/direnv
