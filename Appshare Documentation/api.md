# API Guide

Read your account's data as JSON with https requests

### List of topics

- Get an API token
- Send your requests
- Your account's resources
- Try it with Postman

#### Get an API token

In the web admin, open the **Credentials** tab and enable the API: your token is shown there. It is personal: it reads the data of your account, as you. It expires after a year, and you can generate a new one at any time (the previous one then stops working).

#### Send your requests

Send the token in the `Authorization` header of every request:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" https://api.appshare.site/api/v1/accounts.json
```

A request without a valid token is refused with a 401 status.

#### Your account's resources

Each resource is listed at `https://api.appshare.site/api/v1/<resource>.json`, and one of them at `/api/v1/<resource>/<id>.json`:

| Resource            | What                                           |
|---------------------|------------------------------------------------|
| `accounts`          | your account                                   |
| `users`             | its users                                      |
| `folders`           | its folders and their files                    |
| `uploads`           | the uploads                                    |
| `html_files`        | the logos and html blocks of your website      |
| `meta_tags`         | your pages' meta-tags                          |
| `links`             | your footer's links                            |
| `settings`          | your website's colors                          |
| `csv_files`         | the CSV exports                                |
| `excel_files`       | the Excel exports                              |
| `events`            | your pages' events (visits, downloads)         |
| `daily_events`      | the events, day by day                         |
| `url_daily_events`  | the events, day by day and by page             |

#### Try it with Postman

Download the Postman http client at [postman.com](https://www.postman.com), add your token in the request's **Authorization** tab (type *Bearer Token*), and request your account at [api/v1/accounts](https://api.appshare.site/api/v1/accounts.json).
