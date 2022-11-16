# Beginner Web Hacking Pipeline

The motivation for this project is just how overwhelming it can be to be a beginner in the hacking/Info Sec space. There are so many tools and attacks, and they're all different and genuinely require their own set of expertise. The Lunchbox is meant for curious beginnners. We wanted to create an unintimidating, but robust codebase that could easily be tinkered with by people just learning python for hacking for the first time. We created the project with ease of use, simplicity, and robustneess in mind. With 5 distinct minimalistic GUI's, it's meant to facilitate the process of learning about the core of these attack-types.

# Features
	--Full MITM attack capabilities, including ARP-packet monitoring, spoofing, pcap parsing, and a function to fix the rearranged routing tables.
	--Directory busting, both recurisve and not.
	--HTTP parameter fuzzing, for SQL injections, XSS, or whatever one's fuzzing needs are (just put FUZZ in the URL, supply a wordlist, and watch our fuzzer go to town)
	--HTTP paramter mining, with inspiration from [The Param Spider](https://github.com/devanshbatham/ParamSpider) we use web-archives to extract parameters from domains of your choosing, and format them nicely in a file where you can browse all the valid parameters.
	
# Installation 
''' 
$ Git Clone https://github.com/Noahhw46/The-Lunchbox/ 
$ cd The-Lunchbox 
$ pip install -r requirements.txt 
$ python lunchbox.py 
'''
