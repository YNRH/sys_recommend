#!/bin/sh
set -eo pipefail

if pg_isready -U postgres; then
    exit 0
fi

exit 1
