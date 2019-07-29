# Motion Estimation  

A python program that calculates motion estimation using [macroblock matching](https://en.wikipedia.org/wiki/Block-matching_algorithm).   
  
The program will take a video file as input and generate a new video that displays the movements that will occur in each successive frame.  

Motion estimation is a key part of video compression. By only tracking the elements that change between frames, a lot of redundancy can be removed that can greatly reduce the size of file.

## The Algorithm  

For each frame F<sub>i</sub> in the source video, the frame is split into macroblocks of a user specified size.   

For each of these macroblocks, we search for the block in a 3x3 neighbourhood in frame F<sub>i+1</sub> with the smallest [sum squared distance (SSD)](https://en.wikipedia.org/wiki/Euclidean_distance) above a (user specified) threshold.  
  
If we locate a block in frame F<sub>i+1</sub>, we register that as a matching macroblock and put a red marker in its position in frame F<sub>i</sub> to indicate where that block will move in the next frame.  
  
## Usage  
  
The program takes 3 command-line arguments:  
  
1. The path to the video  
2. The macroblock size (integer)  
3. The motion threshold (integer)  

**Path to the video** <br/>
The output video will be named *source-video-name*_out.mkv and saved in the same folder as the source video.  
  
**Macroblock size** <br/>
A smaller macroblock will predict more precise movements but is more computationally expensive. It is preferred to keep the macroblock size odd for a symmetric neighbourhood search.  
  
**Motion threshold** <br/>
The motion threshold sets the minimum level of contrast required between blocks before they are matched.   
  
This can be set for specific situations, for example a motion threshold of ~10 or less will match very similar blocks, but videos containing lossy compression artifacts will trigger lots of noise.   
  
Conversely a motion threshold of ~40 or greater will only match blocks that are vastly different such as borders of objects, but will not match similar blocks even if there is valid motion.  
  
A motion threshold in-between these extremes will generally give a good result.  
  
Note: adjusting the motion threshold will not affect processing time.   
  
## Demo  
  
The following demo uses a macroblock size of 3, with a motion threshold of 25.  
  
[![Demo](https://i.imgur.com/UqItdcx.png)](https://www.youtube.com/watch?v=hi783etRJG4)
