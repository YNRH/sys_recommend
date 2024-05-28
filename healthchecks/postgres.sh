#!/bin/sh
set -e

if pg_isready -d $POSTGRES_DB -U $POSTGRES_USER; then
  exit 0
fi

exit 1
