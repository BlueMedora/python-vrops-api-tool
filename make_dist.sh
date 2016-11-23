#!/usr/bin/env bash
echo "removing ./build and ./dist"
rm -rf build dist suite-api-tool.dmg
echo "creating app bundle"
cd suite-api-tool && pyinstaller --onefile --windowed --distpath=../dist --workpath=../build ./suite-api-tool.spec && cd ..
echo "removing extra suite-api-tool binary"
rm ./dist/suite-api-tool
echo "creating distribuatble disk image"

disk_size=$(du -hs ./dist | cut -f1)
last=${disk_size: -1}
first=$((${disk_size:0:-1}+1))
disk_size="$first$last"

hdiutil create -size $disk_size -fs HFS+ -volname suite-api-tool ./dist
mv dist.dmg suite-api-tool.dmg
hdiutil unmount /Volumes/suite-api-tool
hdiutil mount suite-api-tool.dmg
cp -r ./dist/* /Volumes/suite-api-tool/
echo "creating link to /Applications"
ln -s /Volumes/suite-api-tool/Applications /Applications
hdiutil unmount /Volumes/suite-api-tool
