# API Guide

Lisez les données de votre compte en JSON avec des requêtes https

### Liste des sujets

- Obtenez un jeton API
- Envoyez vos demandes
- Les ressources de votre compte
- Essayez avec Postman

#### Obtenez un jeton API

Dans l’administrateur web, ouvrez l’onglet **Identifiants** et activez l’API : votre jeton y est affiché. C’est personnel : il lit les données de votre compte, en tant que vous. Il expire après un an, et vous pouvez en générer un nouveau à tout moment (le précédent cesse alors de fonctionner).

#### Envoyez vos demandes

Envoyez le jeton dans l’en-tête `Authorization` de chaque requête :

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" https://api.appshare.site/api/v1/accounts.json
```

Une demande sans jeton valide est refusée avec un statut 401.

#### Les ressources de votre compte

Chaque ressource est listée à `https://api.appshare.site/api/v1/<resource>.json`, et une d’entre elles à `/api/v1/<resource>/<id>.json`:

| Ressource | Quelles |
|---------------------|------------------------------------------------|
| `accounts` | votre compte |
| `users` | ses utilisateurs |
| `folders` | ses dossiers et leurs fichiers |
| `uploads` | les téléchargements |
| `html_files` | les logos et blocs HTML de votre site web |
| `meta_tags` | les méta-balises de vos pages |
| `links` | les liens de votre pied de page |
| `settings` | les couleurs de votre site web |
| `csv_files` | les exportations du CSV |
| `excel_files` | les exportations Excel |
| `events` | les événements de vos pages (visites, téléchargements) |
| `daily_events` | les événements, jour après jour |
| `url_daily_events` | les événements, jour après jour et par page |

#### Essayez avec Postman

Téléchargez le client http Postman à [postman.com](https://www.postman.com), ajoutez votre jeton dans l’onglet **Autorisation** de la requête (tapez *Jeton porteur*), et demandez votre compte à [l’api/v1/accounts](https://api.appshare.site/api/v1/accounts.json).
