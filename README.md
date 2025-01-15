# motion-detection

## Summary
In the past year I've taken a keen interest in Computer Vision and all of the _things_ it's capable of. 

I wanted to synthesize that learning into a simple program for a Raspberry Pi (or anything else, really) that captures motion and sends an alert via email (I want to eventually add SMS support!). It isn't anything groundbreaking and the frame-differencing process is well-documented, but it was something I wanted to do, and maybe someone will find a use for it like I have! :)

## How it works
The program uses a lot of OpenCV's native processing capability and follows the standard flow of image transformation for creating a motion mask. We capture current and previous frames and convert them to grayscale then apply guassian blur (kernel size 9x9) to simplify and smooth out the frames we're looking at. From there we take the absolute difference between frames and then use that difference to create our threshold. Because we are in _grayscale world_ we don't have to deal with anything other than luminance 0-255, making it a simple case of _look at everything above a 20 lum value_ -> everything underneath we treat as black(0), and everything above we convert to white(255).

This both reduces noise and gives us a simple way of determining how much something has changed from frame to frame. 

To me this was hard to visualize until I used a matrix, so I'll show that in-case it's hard for anyone reading this.

Imagine we have a 3x3 matrix of pixels representative of frame1:
```
[10, 10, 10]
[15, 15, 15]
[45, 45, 45]
```

Then we take another 3x3 matrix and it will be representative of frame2:
```
[15, 15, 15]
[20, 20, 20]
[90, 90, 90]
```

Now we look at each coordinate and compare them to look at their difference values:
```
[5,  5,  5]
[5 , 5,  5]
[45, 45, 45]
```

Then we use our thresholding to turn any values under 20 to 0, and any values above 20 to 255:
```
[0,    0,    0]
[0,    0,    0]
[255, 255, 255]
```

Look for the threshold sum, and if that sum is above a certain amount, we keep track in our _detected_ variable to determine for how many frames we see significant movement. Once our breakpoint is reached for that count, we send an email!

## Config/Setup
Provided is a sample .env file that is required for setting up the email alerts. By default this is set to "OFF" and works only by showing what is happening in a OpenCV image rendering window.
If you want to integrate this into anything else you're using feel free, and you can ignore the .env file by leaving it off. 

Note: This program was designed to work on single-camera systems and indexing only accounts for the first camera discovered, hence the constraint. If you want you can go into the code itself and mess with indexing to find the correct camera if you have many.

## Future Plans
- SMS!
- Naming of the camera system (this will be pretty soon it's just not something I thought of initially).
- Storing a captured RGB image when movement is detected
