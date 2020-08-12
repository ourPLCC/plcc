#!/bin/bash

set -ue

# Create a release commit.
standard-version --silent

# Capture the new version.
VERSION="$(git describe --abbrev=0)"

# Create a new (non-release) commit containing a prerelease version number.
standard-version --silent --skip.changelog --skip.tag --prerelease dev

# Print commands for tagging docker images.
echo "# Review CHANGELOG, your git log, and git tags."
echo "# When you are satisfied, run the following commands to publish the release."

VERSION_1_2_3="${VERSION#v}"
VERSION_1_2="${VERSION_1_2_3%.*}"
VERSION_1="${VERSION_1_2%.*}"
IFS=' ' read -ra IMAGES <<< "$IMAGES_TO_RELEASE"
for IMAGE in "${IMAGES[@]}"; do
  BASE="${IMAGE%:*}"
  cat <<EOF
docker tag "${IMAGE}" "${BASE}:${VERSION_1_2_3}" && \\
docker tag "${IMAGE}" "${BASE}:${VERSION_1_2}" && \\
docker tag "${IMAGE}" "${BASE}:${VERSION_1}" && \\
docker tag "${IMAGE}" "${BASE}:latest" && \\
EOF
done

# Print commands to publish git commits and tags
echo "git push --follow-tags origin master && \\"

# Print commands for publishing docker images.
IFS=' ' read -ra IMAGES <<< "$IMAGES_TO_RELEASE"
for IMAGE in "${IMAGES[@]}"; do
  BASE="${IMAGE%:*}"
  cat <<EOF
docker push "${BASE}:${VERSION_1_2_3}" && \\
docker push "${BASE}:${VERSION_1_2}" && \\
docker push "${BASE}:${VERSION_1}" && \\
docker push "${BASE}:latest"
EOF
done
