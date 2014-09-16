#!/bin/bash
XS_ISO_FILE="/srv/isos/hypervisor/XenServer-6.0.201-install-cd.iso"
XS_IMG_SRC="/tmp/xs_img_src"
XS_ISO_MNT="/tmp/xs_iso_mnt"
XS_ISO_REPACK="/tmp/xs_iso_repack"
XS_ISO_NEW="XenServer-6.2.0-install-cd_repack.iso"

echo "umount old iso mount..."
grep -q $XS_ISO_FILE /proc/mounts && umount ${XS_ISO_FILE}
echo "clean old files..."
rm -rf ${XS_IMG_SRC} ${XS_ISO_MNT} ${XS_ISO_REPACK}
rm -f /tmp/install.img /tmp/${XS_ISO_NEW}
echo "mkdir ${XS_IMG_SRC} ${XS_ISO_MNT} ${XS_ISO_REPACK}"
mkdir ${XS_IMG_SRC} ${XS_ISO_MNT} ${XS_ISO_REPACK}
echo "mount -o loop ${XS_ISO_FILE} ${XS_ISO_MNT}/"
mount -o loop ${XS_ISO_FILE} ${XS_ISO_MNT}/
echo "cp -r ${XS_ISO_MNT}/* ${XS_ISO_REPACK}"
cp -r ${XS_ISO_MNT}/* ${XS_ISO_REPACK}
echo "cd ${XS_ISO_REPACK} && rm -f install.img"
cd ${XS_ISO_REPACK} && rm -f install.img
echo "cp ${XS_ISO_MNT}/install.img ${XS_IMG_SRC}/"
cp ${XS_ISO_MNT}/install.img ${XS_IMG_SRC}/
cd ${XS_IMG_SRC}
echo "gunzip -S .img install.img && rm -f install.img"
gunzip -S .img install.img && rm -f install.img
cpio -i < install && rm -f install
echo "set root size to 100GB"
sed -i '/^root_size = /s/4096/102400/' ./opt/xensource/installer/constants.py
echo "set swap size to 4GB"
sed -i '/^swap_size = /s/512/4096/' ./opt/xensource/installer/constants.py
echo "make new iso"
rm -f ../install
find . | cpio -co > ../install
cd /tmp && gzip -S .img -9 install
cp /tmp/install.img ${XS_ISO_REPACK}/ && cd ${XS_ISO_REPACK}
mkisofs -joliet -joliet-long -input-charset utf-8 -r -b ./boot/isolinux/isolinux.bin -no-emul-boot -boot-load-size 4 -boot-info-table -V "XenServer-6.2.0(root_100GB) Base Pack" -o ${XS_ISO_NEW} /tmp/
