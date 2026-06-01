# Static site served by Caddy. Only the site files are copied into the image
# (build scripts, manifest, README stay out of the deployed container).
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY assets /usr/share/caddy/assets
COPY *.html /usr/share/caddy/
