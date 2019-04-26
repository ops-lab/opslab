#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

ROOTPATH=$(cd $(dirname $0); pwd -P)

HOST=x.x.x.x

sed -i "s/ALLOWED_HOSTS.*/ALLOWED_HOSTS = [\"${HOST}\"]/g" ${ROOTPATH}/opslab/opslab/settings.py
sed -i "s/'NAME': 'autosolution'/'NAME': 'auto_solution'/g" ${ROOTPATH}/opslab/opslab/settings.py
sed -i "s/127.0.0.1/${HOST}/g" ${ROOTPATH}/opslab/opslab/settings.py

sed -i "s/127.0.0.1/${HOST}/g" ${ROOTPATH}/opslab/common/utils/insertPermissionToDB.sh
