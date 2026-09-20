#!/bin/sh
# Cerebe CLI installer — checksum-verified binaries onto PATH, then (when
# this is a laptop in a git repo) configure that repo. One line:
#
#   curl -fsSL https://raw.githubusercontent.com/momentiq-ai/cerebe/main/install.sh | sh
#
# Run it from the repo you want adopted. CI (`CI` set) and CEREBE_SKIP_REPO=1
# stay binaries-only. No prompt — curl|sh has no stdin. No local critics.
#
# Env overrides:
#   CEREBE_VERSION=8.4.1     pin a version (default: latest stable release)
#   CEREBE_INSTALL_DIR=DIR   install target (default: /usr/local/bin, or ~/.local/bin
#                            if the former is not writable)
#   CEREBE_SKIP_REPO=1       binaries only, even inside a git repo
set -eu

REPO="momentiq-ai/cerebe"
BINARIES="cerebe cyclone"
VERSION="${CEREBE_VERSION:-}"
VERSION="${VERSION#v}"
# Capture the caller's directory before we cd into the download temp.
# That is the repo the one-liner is supposed to configure.
ORIG_CWD=$(pwd)

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
"$DIR/cerebe" --version || err "just-installed cerebe did not run"
case ":$PATH:" in *":$DIR:"*) : ;; *) printf 'PATH:      add %s to your PATH\n' "$DIR";; esac

# --- this repo (laptop only) ----------------------------------------------
# CI reuses this script for binaries. A prompt cannot work on curl|sh.
if [ -n "${CI:-}" ] || [ -n "${CEREBE_SKIP_REPO:-}" ]; then
  log "Skipping repo setup (CI or CEREBE_SKIP_REPO)."
  exit 0
fi
if ! command -v git >/dev/null 2>&1 \
   || ! git -C "$ORIG_CWD" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf '\nNot a git repository — binaries only.\n'
  printf 'Re-run the same curl from the repo you want adopted.\n'
  exit 0
fi
if [ -f "$ORIG_CWD/cerebe/config.json" ]; then
  log "Configuring this repo (cerebe init — already adopted)."
  (cd "$ORIG_CWD" && "$DIR/cerebe" init)
else
  log "Configuring this repo (cerebe install — empty fleet, no local critics)."
  (cd "$ORIG_CWD" && "$DIR/cerebe" install)
fi
# doctor is the proof the one-liner finished; a blocking row fails the install.
(cd "$ORIG_CWD" && "$DIR/cerebe" doctor)
