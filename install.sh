#!/bin/sh
# Cerebe / Dark Factory CLI installer — downloads the released binaries from
# momentiq-ai/cerebe GitHub Releases, verifies their SHA256 checksums, and
# installs `cerebe` + `cyclone` onto PATH. POSIX sh; macOS + Linux.
#
#   curl -fsSL https://raw.githubusercontent.com/momentiq-ai/cerebe/main/install.sh | sh
#
# Env overrides:
#   CEREBE_VERSION=4.0.0     pin a version (default: latest release)
#   CEREBE_INSTALL_DIR=DIR   install target (default: /usr/local/bin, or ~/.local/bin
#                            if the former is not writable)
set -eu

REPO="momentiq-ai/cerebe"
BINARIES="cerebe cyclone"
VERSION="${CEREBE_VERSION:-}"

log()  { printf '  %s\n' "$*"; }
err()  { printf 'cerebe-install: %s\n' "$*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || err "required tool not found: $1"; }

need curl
need tar
# One of sha256sum / shasum must exist for integrity verification.
if command -v sha256sum >/dev/null 2>&1; then SHACHK="sha256sum -c"; 
elif command -v shasum   >/dev/null 2>&1; then SHACHK="shasum -a 256 -c";
else err "need sha256sum or shasum for checksum verification"; fi

# --- detect os/arch → the GoReleaser asset suffix -------------------------
os=$(uname -s); arch=$(uname -m)
case "$os" in
  Linux)  OS=linux ;;
  Darwin) OS=darwin ;;
  *) err "unsupported OS: $os (Windows: download the .zip from the Releases page)";;
esac
case "$arch" in
  x86_64|amd64) ARCH=amd64 ;;
  arm64|aarch64) ARCH=arm64 ;;
  *) err "unsupported arch: $arch";;
esac
TARGET="${OS}_${ARCH}"

# --- resolve version (default: latest release tag) ------------------------
if [ -z "$VERSION" ]; then
  VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
    | grep '"tag_name"' | head -1 | sed 's/.*"tag_name" *: *"v\{0,1\}\([^"]*\)".*/\1/')
  [ -n "$VERSION" ] || err "could not resolve the latest release version from GitHub"
fi
BASE="https://github.com/${REPO}/releases/download/v${VERSION}"
log "Installing Cerebe CLI v${VERSION} (${TARGET}) from ${REPO} Releases"

# --- install dir (writable, on PATH) --------------------------------------
# An explicit CEREBE_INSTALL_DIR is honored (created if needed). Only the DEFAULT
# (/usr/local/bin) falls back to ~/.local/bin when it is not writable.
if [ -n "${CEREBE_INSTALL_DIR:-}" ]; then
  DIR="$CEREBE_INSTALL_DIR"; mkdir -p "$DIR" || err "cannot create CEREBE_INSTALL_DIR=$DIR"
  [ -w "$DIR" ] || err "CEREBE_INSTALL_DIR=$DIR is not writable"
else
  DIR="/usr/local/bin"
  if [ ! -d "$DIR" ] || [ ! -w "$DIR" ]; then
    DIR="$HOME/.local/bin"; mkdir -p "$DIR"
    log "Note: /usr/local/bin not writable → installing to $DIR (ensure it is on PATH)"
  fi
fi

# --- download + verify + extract each binary ------------------------------
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; cd "$tmp"
curl -fsSLO "${BASE}/checksums.txt" || err "could not download checksums.txt for v${VERSION}"
for bin in $BINARIES; do
  asset="${bin}_${VERSION}_${TARGET}.tar.gz"
  log "→ ${asset}"
  curl -fsSLO "${BASE}/${asset}" || err "download failed: ${asset}"
  # Materialize THIS asset's checksum line; fail hard if absent (an empty grep
  # piped to the checker can exit 0), then verify, then extract.
  grep " ${asset}\$" checksums.txt > "${asset}.sha256" \
    || err "no checksum entry for ${asset} — refusing to install unverified"
  [ -s "${asset}.sha256" ] || err "empty checksum entry for ${asset}"
  $SHACHK "${asset}.sha256" >/dev/null || err "checksum mismatch for ${asset} — refusing to install"
  tar -xzf "$asset" "$bin"
  chmod 0755 "$bin"
  mv -f "$bin" "$DIR/$bin"
done

printf '\nInstalled: %s → %s\n' "$BINARIES" "$DIR"
printf 'Verify:    cerebe --version   (expect v%s)\n' "$VERSION"
case ":$PATH:" in *":$DIR:"*) : ;; *) printf 'PATH:      add %s to your PATH\n' "$DIR";; esac
