#!/bin/bash

if [ -z "$1" ] ; then
    echo 'Bitte Quell-CSV-Datei angeben!'
    exit 1
fi

if [ -z "$2" ] ; then
    echo 'Bitte Ausgabeverzeichnis für OFX angeben!'
    exit 1
fi


filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"
CSVModAusgabePfad=$(dirname $1)
CSVModAusgabedatei="${CSVModAusgabePfad}/${filename}_mod.csv"

# Zeilen oberhalb des CSV-Headers entfernen:
tail -n +6 $1 > ${CSVModAusgabedatei} 


OFXAusgabedatei=$2/$filename.ofx
ofxstatement convert -t consors ${CSVModAusgabedatei} "$OFXAusgabedatei"
#ofxstatement convert -t consors ${CSVModAusgabedatei} test.ofx




# Ansatz mit CSV:
# http://homebank.free.fr/help/misc-csvformat.html
# TODO: Parameter einlesen: Dateiname und Ausgabepfad (basename!) 
# 1. Obere Zeilen entfernen: https://www.baeldung.com/linux/remove-first-line-text-file
# 2. Seperator in CSV ändern: csvtool -t ',' -u ';' cat Umsatzübersicht_380333703_2024_01_11.csv -o Umsatzübersicht_380333703_2024_01_11_5.csv
# 3. awk 'BEGIN{FS=OFS=";"} {$NF=0} 1' deine_datei.csv > neue_datei.csv bzw. https://stackoverflow.com/questions/7551991/add-a-new-column-to-the-file
# 4. Spalten anordnen https://github.com/maroofi/csvtool


