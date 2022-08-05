# Instagram

For Windows only

```bash
> cd Desktop
> git clone https://github.com/Arif-Helmsys/Pyinsta.git
> pip install -r .\Pyinsta\requirements.txt
```
*First Login*
```bash
> python .\Pyinsta\app.py -u <username> -p <password>
```
*Every entry for the next*
```bash
> python .\Pyinsta\app.py
```

As you can see in our command line, there is a "$" sign. It says it's on our main command line. If this sign is "#", it informs that we will take action on the previous line. I give an example;

<img src="https://i.hizliresim.com/1hfqzis.png" width=60% height=60%>
In the link specified as the post thumbnail, there is the link of the most recent post. It was too long so I scraped it at the back and converted it to a short urly.

Now I will show you how to read a message from DM.
This dm read only reads the top message (without leaving it seen). I guess I need to apply a different action to read other messages.

<img src="https://i.hizliresim.com/23a1z8r.jpg" width=60% height=60%>

- It creates a folder named "PyInsta" in the "Documents" folder on our computer. If you want to delete it after using it, you can delete the folder mentioned in the path I mentioned yourself.

# BruteForce
```bash
> python .\Pyinsta\app.py -v user_name -w wordlist.txt -px http
```
```bash
> python .\Pyinsta\app.py -v user_name -w wordlist.txt -px socks4
```
```bash
> python .\Pyinsta\app.py -v user_name -w wordlist.txt -px socks5
```


It will be developed over time...
