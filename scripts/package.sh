#!/usr/bin/env bash
set -euo pipefail

# Create a distributable tarball excluding .git and .venv
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DST="$ROOT_DIR/SelfCraft-Media-Editor.tar.gz"

echo "Packaging into $DST"
cd "$ROOT_DIR"
STAGING=$(mktemp -d)
PAYLOAD_DIR="sme_files"

echo "Copying project into staging ($STAGING/$PAYLOAD_DIR)..."
mkdir -p "$STAGING/$PAYLOAD_DIR"
shopt -s dotglob
for f in *; do
	if [ "$f" = "SelfCraft Media Editor.bat" ]; then
		continue
	fi
	if [ "$f" = ".git" ] || [ "$f" = ".venv" ] || [ "$f" = "dist" ]; then
		continue
	fi
	cp -a "$f" "$STAGING/$PAYLOAD_DIR/"
done

echo "Creating uncompressed tar with payload..."
UNCOMP="$DST.uncompressed"
tar -C "$STAGING" -cf "$UNCOMP" "$PAYLOAD_DIR"

echo "Appending launcher at root into tarball..."
tar --append --file="$UNCOMP" -C "$ROOT_DIR" "SelfCraft Media Editor.bat"

echo "Compressing tarball..."
gzip -c "$UNCOMP" > "$DST"
rm -f "$UNCOMP"

echo "Created: $DST"
rm -rf "$STAGING"
