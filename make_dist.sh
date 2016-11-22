#!/usr/bin/env bash
rm -rf build dist
cd suite-api-tool && pyinstaller --onefile --windowed --distpath=../dist --workpath=../build ./suite-api-tool.spec
