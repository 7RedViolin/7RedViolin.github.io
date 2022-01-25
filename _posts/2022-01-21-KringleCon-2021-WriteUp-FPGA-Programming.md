---
layout: page
title: "KringleCon 4: Four Calling Birds WriteUp - FPGA Programming"
date: 2022-01-21 21:00:00 -0500
tags: ctf kringlecon-2021 iot
intro: Frequency changing via FPGA programming
---

## Objective: FPGA Programming
> Write your first FPGA program to make a doll sing.

In this challenge, we get to use FPGA programming to alter a given a consisten clock frequency input to manipulate sound.

Having never worked with FPGA or embedded systems, I watched Prof. Qwerty Petabyte's lecture and took some notes:
- Hardware Description Language (HDL) is not the same a traditiona programming (e.g. python or c++)
- Relies on specific events like clock edges, board resets, and power cycles rather than logic loops.
- Registers are used instead of variables
- Inputs and outputs have to be tied to real-world things lick clock counters, hardware, etc.
- All HDL activity occurs in parallel
- A sample program was given at 4:52 that shows how to adjust the frequency of a 100MHz clock

Then, for this specific challenge, we're given additional info:
- The input clock frequency is 125MHz (aka 125,000,000Hz)
- The target frequency will be formated as NNNNDD which should be interpreted as NNNN.DD
- The output square wave should alternate between 1 and 0.
- To test the program works as expected, it will have to produce the following waves: 500Hz, 1kHz, 2kHz, and a random frequency.

Doing a bit of math, 
- The target frequency will need to be divided by 100 so we can covert NNNNDD to NNNN.DD
- The overall result must be divided by 2 so we get a square wave that alternates between 1 and 0 in a complete cycle
- To make sure we switch between 1 and 0 at the right moment, we need to divide 125,000,000 by the target frequency to get the appropriate cycle.

In summary: `(125,000,000/(freq/100))/2 = 125,000,000/(freq * 0.02)`

Since the above formula will only give integers for certain numbers, we'll need to round the results. At the beginning of the terminal, we're given the hint `If $rtoi(real_no * 10) - ($rtoi(real_no) * 10) > 4, add 1`. Translated, it means this:
- `real_no * 10` = Basically moves the decimal one space to the right (e.g. 2.3 becomes 23)
- `$rtoi()` = Converts a real number to an integer (e.g. 2.34 becomes 2)
- `$rtoi(real_no * 10)` = Converts to an integer after moving the decimal one space to the right (e.g. 2.34 becomes 23)
- `$rtoi(real_no) * 10` = Moves the decimal two spaces after converting to an integer (e.g. 2.345 becomes 20)
- By subtracing the two previous operations, we pull out the decimal value (e.g. 23 - 20 = 3). If the result is greater than four, we round up one. Otherwise, we leave the number as-is.

Using the sample program from the YouTube video and the above math, we're able to dynamically alter the clock frequency.

```
// Note: For this lab, we will be working with QRP Corporation's CQC-11 FPGA.
// The CQC-11 operates with a 125MHz clock.
// Your design for a tone generator must support the following 
// inputs/outputs:
// (NOTE: DO NOT CHANGE THE NAMES. OUR AUTOMATED GRADING TOOL
// REQUIRES THE USE OF THESE NAMES!)
// input clk - this will be connected to the 125MHz system clock
// input rst - this will be connected to the system board's reset bus
// input freq - a 32 bit integer indicating the required frequency
//              (0 - 9999.99Hz) formatted as follows:
//              32'hf1206 or 32'd987654 = 9876.54Hz
// output wave_out - a square wave output of the desired frequency
// you can create whatever other variables you need, but remember
// to initialize them to something!

`timescale 1ns/1ns
module tone_generator (
    input clk,
    input rst,
    input [31:0] freq,
    output wave_out
);
    // ---- DO NOT CHANGE THE CODE ABOVE THIS LINE ---- 
    // ---- IT IS NECESSARY FOR AUTOMATED ANALYSIS ----
    reg [31:0] counter;
    reg result_wave;
    reg [31:0] limit;
    assign wave_out = result_wave;
    
    always @(posedge clk or posedge rst)
    begin
        // Here is where we check the cycle to see if it needs to be rounded up or not
        if ($rtoi(1250000000/(freq*0.02) * 10) - ($rtoi(1250000000/(freq*0.02)) * 10) > 4)
            // Rounding up by one
            limit <= $rtoi(1250000000/(freq*0.02) + 1);
        else
            // Leaving the cycle as-is
            limit <= $rtoi(125000000/(freq*0.02));

        if (rst==1)
            // Start with the wave being 0 when we first start the device
            begin
                counter <= limit;
                result_wave <= 0;
            end
        else
            if (counter == 0)   // If the limit has been reached, switch to the opposite signal
                begin
                    counter <= limit - 1;
                    result_wave <= result_wave ^ 1'b1;
                end
            else                // Otherwise, keep counting down to zero
                counter <= counter - 1;;
    end
endmodule
```

To see my other writeups for this CTF, check out the tag [#kringlecon-2021](/tags#kringlecon-2021).

## References
- [Prof. Qwerty Petabyte's lecture](https://www.youtube.com/watch?v=GFdG1PJ4QjA)