# Guía API

Lee los datos de tu cuenta en JSON con peticiones https

### Lista de temas

- Consigue un token API
- Envía tus solicitudes
- Recursos de tu cuenta
- Pruébalo con Postman

#### Consigue un token API

En el administrador web, abre la pestaña **Credenciales** y activa la API: tu token aparece ahí. Es personal: lee los datos de tu cuenta, como tú. Caduca tras un año, y puedes generar uno nuevo en cualquier momento (el anterior deja de funcionar).

#### Envía tus solicitudes

Envía el token en la cabecera `Authorization` de cada petición:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" https://api.appshare.site/api/v1/accounts.json
```

Una solicitud sin un token válido es rechazada con un estado 401.

#### Recursos de tu cuenta

Cada recurso está listado en `https://api.appshare.site/api/v1/<resource>.json`, y uno de ellos en `/api/v1/<resource>/<id>.json`:

| Recurso | Qué |
|---------------------|------------------------------------------------|
| `accounts` | tu cuenta |
| `users` | sus usuarios |
| `folders` | sus carpetas y sus archivos |
| `uploads` | las subidas |
| `html_files` | los logotipos y bloques HTML de tu sitio web |
| `meta_tags` | las meta-etiquetas de tus páginas |
| `links` | los enlaces de tu pie de página |
| `settings` | los colores de tu sitio web |
| `csv_files` | exportaciones de CSV |
| `excel_files` | las exportaciones de Excel |
| `events` | los eventos de tus páginas (visitas, descargas) |
| `daily_events` | los acontecimientos, día a día |
| `url_daily_events` | los acontecimientos, día a día y por página |

#### Pruébalo con Postman

Descarga el cliente http de Postman en [postman.com](https://www.postman.com), añade tu token en la pestaña **de Autorización** de la solicitud (escribe *Token Portador*) y solicita tu cuenta en [api/v1/accounts](https://api.appshare.site/api/v1/accounts.json).
