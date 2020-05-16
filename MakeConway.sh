echo "John Horton Conway  1937-2020" >/tmp/jhc_1.txt
echo "SketchyMachines project 15-APR-2020" >/tmp/jhc_2.txt
python PlotterTests/text2lines.py futural /tmp/jhc_1.txt /tmp/jhc_1.lines
python PlotterTests/text2lines.py cursive /tmp/jhc_2.txt /tmp/jhc_2.lines
echo "500 500 8000 500 8000 10500 500 10500 500 500" >/tmp/outerframe.lines

python PlotterTests/compositelines.py --fix_aspect /tmp/outerframe.lines 0 0.05 1 .075 /tmp/jhc_1.lines /tmp/tmp.lines
mv /tmp/tmp.lines /tmp/output.lines
python PlotterTests/compositelines.py --fix_aspect /tmp/output.lines 0.35 0.01 1 .035 /tmp/jhc_2.lines /tmp/tmp.lines
mv /tmp/tmp.lines /tmp/output.lines
python PlotterTests/compositelines.py --fix_aspect /tmp/output.lines 0.05 0.075 0.95 0.95 Drawings/Conway/conway_cleaned.lines /tmp/tmp.lines
mv /tmp/tmp.lines /tmp/output.lines
python PlotterTests/lines2render.py /tmp/output.lines 500 500 8000 10500 conway.hpgl


