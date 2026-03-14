#!/usr/bin/env bash
# scripts/test_docker.sh
#
# Build a Docker image for each target OS and run the integration test suite
# inside it.  Exit code is 0 only if every image passes.
#
# Usage:
#   ./scripts/test_docker.sh                   # test all targets
#   ./scripts/test_docker.sh ubuntu fedora     # test specific targets
#
# Requirements: Docker must be installed and the daemon must be running.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_DIR="$REPO_ROOT/docker"
IMAGE_PREFIX="magicprobe-test"

# All supported targets (name maps to docker/<name>.Dockerfile)
ALL_TARGETS=(ubuntu debian alpine fedora)

# --------------------------------------------------------------------------
# Resolve which targets to run
# --------------------------------------------------------------------------
if [[ $# -gt 0 ]]; then
    TARGETS=("$@")
else
    TARGETS=("${ALL_TARGETS[@]}")
fi

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
passed=()
failed=()

run_target() {
    local name="$1"
    local dockerfile="$DOCKER_DIR/${name}.Dockerfile"
    local image="${IMAGE_PREFIX}-${name}"

    if [[ ! -f "$dockerfile" ]]; then
        echo "⚠️  Skipping '$name': $dockerfile not found."
        return
    fi

    echo ""
    echo "════════════════════════════════════════"
    echo "  Building: $name"
    echo "════════════════════════════════════════"

    if docker build \
            --file "$dockerfile" \
            --tag  "$image" \
            --quiet \
            "$REPO_ROOT"; then

        echo "  Running tests inside $name …"
        if docker run --rm "$image"; then
            passed+=("$name")
            echo "  ✅  $name PASSED"
        else
            failed+=("$name")
            echo "  ❌  $name FAILED (tests)"
        fi
    else
        failed+=("$name")
        echo "  ❌  $name FAILED (build)"
    fi
}

# --------------------------------------------------------------------------
# Run each target
# --------------------------------------------------------------------------
for target in "${TARGETS[@]}"; do
    run_target "$target"
done

# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------
echo ""
echo "════════════════════════════════════════"
echo "  Results"
echo "════════════════════════════════════════"

for t in "${passed[@]+"${passed[@]}"}"; do
    echo "  ✅  $t"
done
for t in "${failed[@]+"${failed[@]}"}"; do
    echo "  ❌  $t"
done

if [[ ${#failed[@]} -gt 0 ]]; then
    echo ""
    echo "Some targets failed: ${failed[*]}"
    exit 1
fi

echo ""
echo "All targets passed."
exit 0
