# tumblr-dl
Use the Tumblr API to download images from a blog, with optional tags and note count requirements

## Usage
```
usage: tumblr-dl.py [-h] [-nc NOTES] [-t TAG] blog

positional arguments:
  blog                  tumblr blog to scrape

optional arguments:
  -h, --help            show this help message and exit
  -nc, --notes          only download images with >= this note count
  -t, --tag             only download images with this tag
```

## Examples
Download *all* images from the fictional blog makebaseballgreatagain.tumblr.com  
`tumblr-dl.py makebaseballgreatagain`  

Download images with a note count of at least 100  
`tumblr-dl.py makebaseballgreatagain -nc 100`  

Download images with the tag "homerun"  
`tumblr-dl.py makebaseballgreatagain -t homerun` 

Download images with the tag "homerun" *and* a note count of at least 100  
`tumblr-dl.py makebaseballgreatagain -t homerun -nc 100`  

## Requirements  
1. Python 3.6  
2. requests library `pip install requests`  

## Config
This script uses the Tumblr API so you'll need an API key.  
This can be obtained by using the [Tumblr API Console](https://api.tumblr.com/console).  

Next, create a config file (e.g. `api_key.txt`) in the same directory as tumblr-dl.py.  
The API key should be the first and only line of the config file.  

Finally, insert the path of this config file into the `CONFIG` variable of tumblr-dl.py.  

```CONFIG = 'api_key.txt'```
