# Treava V. Barnes website

A Django website based on the supplied client HTML and artwork. Product and booking links open the client's existing services. Free-tools signups and coaching requests are validated on the server and stored in SQLite for review in Django admin.

The site uses the original attached HTML's purple, white, and blush palette, Fraunces and Instrument Sans fonts, rounded cards, and brass borders. That source is preserved in `reference/original-design.html`; its stylesheet is kept unchanged in `static/website/css/reference.css`. The original hero grid and brass arched mirror, biography/facts columns, book/pricing columns, card spacing, and mobile breakpoint are restored. Four text-free WebP backgrounds complement that layout, with complete book and guide covers shown as product images. Headings, prices, and buttons remain editable HTML. The pre-existing `Treava_V_Barnes_Luxury_Redesign.html` is retained as an unused reference.

The backgrounds are crops and compositions of the supplied photo areas and downloaded client artwork, rather than AI-generated replacements. All original images are retained. No API key is required to run the website or rebuild these backgrounds.

The Digital Hub product section follows the supplied flyer: complete covers on the left and stacked cream product cards on the right, with metallic gold borders, circular gold icons, dark red prices, and burgundy order buttons. Its styles are in `static/website/css/products.css`.

The Digital Hub product section follows the supplied flyer: complete covers on the left and stacked cream product cards on the right, with metallic gold borders, circular gold icons, dark red prices, and burgundy order buttons. Its styles are in `static/website/css/products.css`.

## Run locally on Windows

An existing virtual environment is included in this workspace. From `E:\Django\Treava` in PowerShell:

```powershell
.\env\Scripts\python.exe manage.py migrate
.\env\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/>.

For a fresh checkout, create a virtual environment and install the pinned dependencies first:

```powershell
python -m venv env
.\env\Scripts\python.exe -m pip install -r requirements.txt
```

## Review submissions

Create an administrator account interactively:

```powershell
.\env\Scripts\python.exe manage.py createsuperuser
```

Open <http://127.0.0.1:8000/admin/> to review **Free tools signups** and **Coaching requests**. No administrator password is embedded in the project. Forms save requests; automatic email delivery and downloadable free tools are not configured because those files and mail credentials were not supplied.

## Project files

- `templates/website/home.html`: website content and Django form integration.
- `static/`: styles, scripts, and supplied artwork.
- `website/`: submission models, forms, views, admin, and tests.
- `treava/settings.py`: environment-aware Django configuration.
- `db.sqlite3`: local database created by migrations; excluded from version control.

## Background artwork

- `static/website/images/backgrounds/`: four optimized backgrounds, each 2048 × 1152 pixels.
- `static/website/images/products/`: complete book and guide covers, plus the portrait used in the original arched frame.
- `static/website/images/linktree/`: all 23 public client images downloaded from <https://linktr.ee/IamTreavaBarnes>, including listing images and linked preview artwork.
- `reference/linktree-images.json`: source URLs, filenames, dimensions, and sizes for the 23 downloads.
- `reference/background-assets.json`: source crop coordinates and output details for the four backgrounds.
- `reference/product-assets.json`: source images and output details for the book, guides, and portrait.
- `reference/background-contact-sheet.jpg`: a visual inventory of the four finished backgrounds.

Pillow is only needed for the optional artwork scripts; Django serves the finished files without it. To rebuild the backgrounds from the retained source images:

```powershell
.\env\Scripts\python.exe -m pip install Pillow==13.0.0
.\env\Scripts\python.exe scripts\build_backgrounds.py
.\env\Scripts\python.exe scripts\prepare_product_assets.py
```

The public downloads can be refreshed from the saved Linktree page data using `scripts/import_linktree_images.py`. That script needs Pillow and network access. The site itself uses local assets and does not fetch its backgrounds from Linktree at runtime.

## Validate

```powershell
.\env\Scripts\python.exe manage.py check
.\env\Scripts\python.exe manage.py test
```

## Deployment settings

Settings read process environment variables; `.env.example` documents the variables and is not automatically loaded. Set `DJANGO_DEBUG=0`, a unique `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` to the live domain, and `DJANGO_CSRF_TRUSTED_ORIGINS` to its full HTTPS origin. Secure session and CSRF cookies and HTTP-to-HTTPS redirection are enabled when debug is off. A reverse proxy must pass the request scheme correctly; configure its trusted proxy settings for your deployment.

Run `manage.py collectstatic`, serve `staticfiles/` using the web server, and run the WSGI or ASGI application through a production application server. Django's development server is for local use. Back up the SQLite database or configure a production database appropriate for your hosting environment.
