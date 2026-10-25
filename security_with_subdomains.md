### Security with subdomains: assessment and proposals

#: 1
Change: Session cookie Secure
Why: The backend's session_id cookie is missing the Secure flag, so a browser could
send it over plain HTTP.
Effort: tiny
Where: backend
────────────────────────────────────────
#: 2
Change: HSTS includeSubDomains
Why: Browsers would then refuse plain HTTP on every *.appshare.site, including new
client sites. Now safe, since the wildcard goes through Cloudflare's HTTPS.
Effort: tiny
Where: 4 nginx configs
────────────────────────────────────────
#: 3
Change: CORS limited to appshare.site and *.appshare.site
Why: Today origins '*' lets any website call the API from a visitor's browser. The
desktop apps send no Origin, so they're unaffected.
Effort: small
Where: backend (+ stream)
────────────────────────────────────────
#: 4
Change: Block look-alike addresses
Why: Reject punycode (xn--…, used for homograph phishing such as a Cyrillic "аpple"),
and reserve names like secure, verify, paypal, google and appshare-*, so nobody can
register a convincing phishing page on your domain.
Effort: small
Where: backend
────────────────────────────────────────
#: 5
Change: Tighter Content-Security-Policy on the sites
Why: Remove 'unsafe-inline' scripts: the only inline script in index.html is dead code
(a service-worker snippet running in the page). Also limit connect-src to the API,
stream and Azure storage. The sites display user content, so this strongly limits
damage from any XSS.
Effort: medium (needs browser testing)
Where: frontend
────────────────────────────────────────
#: 6
Change: Rate-limit the address check
Why: register.appshare.site/subdomain_availability is public and calls the backend with
a privileged token. Best done as a Cloudflare rate-limiting rule: the free plan
includes one. The apps only see the router's IP, so limiting by IP in Rails wouldn't
work.
Effort: small, in Cloudflare (I'll give you the exact rule)
Where: Cloudflare
────────────────────────────────────────
#: 7
Change: Authenticated Origin Pulls
Why: Your origin accepts HTTPS from anyone who finds its IP, bypassing Cloudflare. This
makes nginx accept only Cloudflare's client certificate, which then also makes it
safe to trust CF-Connecting-IP for real visitor IPs in logs and limits.
Effort: medium
Where: nginx-frontend + Cloudflare
────────────────────────────────────────
#: 8
Change: Public Suffix List entry for appshare.site, longer term
Why: Browsers would then treat each client site as a separate site, not just a separate
origin, which is what github.io and vercel.app do for user content. It's a pull
request to the public list, takes weeks, and changes cookie behavior, so it's worth
discussing first.
Effort: process
Where: —

