# produce plots
rm -f output/*.png && ./electricCarEfficiency.py && ls -lh output/ && open ./output/*.png
# ./electricCarEfficiency.py && ls -lh output/ 
# produce slides
cd slides && pdflatex electricCarEfficiency.tex && open electricCarEfficiency.pdf && cd ..
