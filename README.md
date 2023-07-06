# Instagram

For Windows only

```bash
> cd Desktop
> git clone https://github.com/Arif-Helmsys/Pyinsta.git
> cd Pyinsta
> pip install -r requirements.txt
```
```
> python app.py -h
...
usage: app.py [-h] [-u USERNAME] [-p PASSWORD] [-px PROXY] [-v VICTIM] [-w WORDLIST] [-t THREAD]
              [-b] [--create-account]

How to Using

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Instagram Username
  -p PASSWORD, --password PASSWORD
                        Instagram Password
  -px PROXY, --proxy PROXY
                        Specify proxy type [socks4, socks5, http] or write the proxy file you have
  -v VICTIM, --victim VICTIM
                        Victim username
  -w WORDLIST, --wordlist WORDLIST
                        Specify wordlist path
  -t THREAD, --thread THREAD
                        Specify Number of Threads [4, 5, 6, ..., 40, ...]
  -b, --brute-force
  --create-account      Create Instagram Multi Account

First time to login to Instagram > python app.py -u my_user_name -p my_password
```

*First Login*
```bash
> python app.py -u <username> -p <password>
```
*Every entry for the next*
```bash
> python app.py
```

As you can see in our command line, there is a "$" sign. It says it's on our main command line. If this sign is "#", it informs that we will take action on the previous line. I give an example;

<img src="https://i.hizliresim.com/1hfqzis.png" width=60% height=60%>
In the link specified as the post thumbnail, there is the link of the most recent post. It was too long so I scraped it at the back and converted it to a short urly.

Now I will show you how to read a message from DM.
This dm read only reads the top message (without leaving it seen). I guess I need to apply a different action to read other messages.

<img src="https://i.hizliresim.com/23a1z8r.jpg" width=60% height=60%>

- It creates a folder named "PyInsta" in the "Documents" folder on our computer. If you want to delete it after using it, you can delete the folder mentioned in the path I mentioned yourself.

# BruteForce For Instagram
```
> python app.py -b
-t/--thread   : THREAD Number
-w/--wordlist : WORDLIST
-v/--victim   : VICTIM
-px/--proxy   : PROXY TYPE ['http','socks4','socks5'] or PROXY FILE

python app.py -v user_name -w wordlist.txt -px proxy_file.txt -t 40
```

[![Hits](https://hits.sh/github.com/Arif-Helmsys/Pyinsta.svg?label=views&color=007ec6)](https://hits.sh/github.com/Arif-Helmsys/Pyinsta/)
