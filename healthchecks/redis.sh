#!/bin/sh
set -e

if redis-cli ping | grep -q "PONG"; then
  exit 0
fi

exit 1
