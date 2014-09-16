#!/bin/bash
XS_ISO_FILE="/mnt/isos/hypervisor/XenServer-6.0.201-install-cd_100G.iso"
XS_ISO_MNT="/tmp/xs_iso_mnt"
XS_ISO_REPACK="/tmp/xs_iso_repack"
XS_ISO_NEW="XenServer-6.0.201-install-cd_repack.iso"

umount ${XS_ISO_MNT}
rm -rf ${XS_ISO_MNT} ${XS_ISO_REPACK}
rm -f /tmp/install.img /tmp/${XS_ISO_NEW}

mkdir ${XS_ISO_MNT} ${XS_ISO_REPACK}
mount -o loop ${XS_ISO_FILE} ${XS_ISO_MNT}/
cp -r ${XS_ISO_MNT}/* ${XS_ISO_REPACK}
cd ${XS_ISO_REPACK} && rm -f install.img
