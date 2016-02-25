import os
import urllib
 
root = "/var/log/apache2"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} # Curly braces define empty dictionary
urls = {}
user_bytes = {}

total = 0
import gzip
for filename in os.listdir(root):
    if not filename.startswith("access.log"):
        continue
    if filename.endswith(".gz"):
        fh = gzip.open(os.path.join(root, filename))
    else:
        fh = open(os.path.join(root, filename))
    print "Parsing:", filename
    for line in fh:
        total = total + 1
        try:
            source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
            method, path, protocol = request.split(" ")
        except ValueError:
            continue # Skip garbage
            
        if path == "*": continue # Skip asterisk for path

        _, status_code, content_length, _ = response.split(" ")
        content_length = int(content_length)
        path = urllib.unquote(path)
        
        if path.startswith("/~"):
            username = path[2:].split("/")[0]
            try:
                user_bytes[username] = user_bytes[username] + content_length
            except:
                user_bytes[username] = content_length

        try:
            urls[path] = urls[path] + 1
        except:
            urls[path] = 1
        
        for keyword in keywords:
            if keyword in agent:
                try:
                    d[keyword] = d[keyword] + 1
                except KeyError:
                    d[keyword] = 1
                break

print
print("Top 5 bandwidth hoggers:")
results = user_bytes.items()
results.sort(key = lambda item:item[1], reverse=True)
for user, transferred_bytes in results[:5]:
    print user, "==>", transferred_bytes / (1024 * 1024), "MB"
    
print
print("Top 5 visited URL-s:")
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for path, hits in results[:5]:
    print "http://enos.itcollege.ee" + path, "==>", hits, "(", hits * 100 / total, "%)"

