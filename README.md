# Minecraft ore analysis

## Let's see how the new cave update ore generation compares to the old!

## Go to https://npc-strider.github.io/cave-update-ore-analysis for interactive graphs!

### Both tests performed with seed 0 and single biome mode enabled (Extreme hills biome only, to include emerald ore statistics). Size of 1024*1024 scanned.

### Original world files used for research are located at https://drive.google.com/drive/folders/1RsmfDp4nl5KaFWfCpL5sanK6cGUp45TO?usp=sharing

#

The scripts I've created take advantage of a slightly modified [PyAnvilEditor](https://github.com/DonoA/PyAnvilEditor) to parse the region files.

I've replaced the code in the `276` (and everything else under `def close(self):`) of the `world` class of PyAnvilEditor with `true` - this is because I'm not writing to the world file, I only intend to read from it. This saves a large amount of time spent writing that would go to waste.

To generate the graphs I've used Matplotlib and I use mpld3 to convert these graphs into interactive html files for use on my website.

We load a large section of the world into memory - ideally, you want to set the block size to the maximum as this is quicker than loading small sections of the world repeatedly. Then we iterate through each coordinate in the block - this takes about 90 seconds with a block radius of `128`. At each coordinate we iterate each count for a tile in a particular layer. Once a whole block has been processed, we add it to the total.

The 'sum' represents the total amount of a particular ore block within the whole sample (A 1024*1024 square meter area). The relative frequency represents the proportion of the total amount of a particular ore that occurs at a particular y-level.

This sample size can be improved on but it would obviously take longer given that my RAM is limited.