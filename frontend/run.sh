#!/bin/sh
set -e

if [ "$APP_DEBUG" = "true" ]; then
    exec npm run dev
else
    npm run build
    exec node .output/server/index.mjs
fi
