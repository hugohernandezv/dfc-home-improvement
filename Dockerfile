# Static site served by Caddy. Only the site files are copied into the image
# (build scripts, manifest, README stay out of the deployed container).
FROM caddy:2-alpine
# cache-bust 2026-06-10: a prior build shipped without review.html though it was
# in the source commit; this line forces the COPY layers below to rebuild clean.
ARG CACHE_BUST=2026-06-10-1
COPY Caddyfile /etc/caddy/Caddyfile
COPY assets /usr/share/caddy/assets
COPY *.html /usr/share/caddy/
# Subfolder pages (e.g. /cost/*) — *.html above only matches the root level,
# so each content subdirectory must be copied explicitly or it 404s in prod.
COPY cost /usr/share/caddy/cost
