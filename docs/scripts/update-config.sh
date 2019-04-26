#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

ROOT_PATH=$(cd $(dirname $0)/../..; pwd -P)

HOST=x.x.x.x

sed -i "s/127.0.0.1/${HOST}/g" ${ROOTPATH}/opslab/common/utils/insertPermissionToDB.sh
sed -i "s/127.0.0.1/${HOST}/g" ${ROOTPATH}/opslab/opslab/settings.py
sed -i "s/'NAME': 'autosolution'/'NAME': 'auto_solution'/g" ${ROOTPATH}/opslab/opslab/settings.py
