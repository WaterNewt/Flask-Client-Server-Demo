import sys
import time
import json
import pygame
import hashlib
import requests
from statistics import mean

def md5_hash(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

pygame.init()

try:
    host = sys.argv[1]
except:
    print("Please specify server host IP as first arg.")
    sys.exit(0)
try:
    username = sys.argv[2]
except:
    print("Please specify username as second arg.")
    sys.exit(0)
    
print("Testing server...")
latencies = []
interval = 0
for i in range(3):
    start = time.time()
    requests.get('http://'+host)
    duration = (time.time()-start)*100
    latencies.append(duration)
mean_latency = mean(latencies)
write_margin = 50
read_margin = 30
width, height = 400, 300
cube_size = 30
center = [(width-cube_size)//2, (height-cube_size)//2]
write_interval = (mean_latency+write_margin)/100
read_interval = (mean_latency+read_margin)/100
print(f"Average latency: {str(int(mean_latency))}")
print(f"Using interval: {str(interval)}")

def logoff():
    print("Sending logoff...")
    logoff = requests.get('http://'+host+"/log/false?username="+username)
    print("Logged off.")
    return logoff.text
with requests.get("http://"+host+"/getplayer?username="+username) as f:
    if f.status_code==200:
        this_player = f.json()
    elif f.status_code==401:
        this_player = requests.post('http://'+host+"/newuser", json={"username": username, "pos": center}, headers={"Content-Type": 'application/json'}).json()
    else:
        print(f.text)
        sys.exit(1)
with requests.get("http://"+host+"/getworld") as f:
    world:dict = f.json()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption(username)

move_speed = 5

running = True
last_write = time.time()
last_read = time.time()
fake_pos = this_player['pos']
print("Logging in...")
logon = requests.get('http://'+host+"/log/true?username="+username)

if not logon.status_code==200:
    print("\n"+logon.json()['message'])
    sys.exit(1)

while running:
    try:
        if (time.time()-last_read)>=read_interval:
            start = time.time()
            with requests.get("http://"+host+"/getworld") as f:
                world:dict = f.json()
            interval = (time.time()-start)*100
            latencies.append(interval)
            last_read = time.time()
        window.fill(world['game']['bg'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logoff()
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            fake_pos[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            fake_pos[0] += move_speed
        if keys[pygame.K_UP]:
            fake_pos[1] -= move_speed
        if keys[pygame.K_DOWN]:
            fake_pos[1] += move_speed
        if (time.time()-last_write)>=write_interval:
            start = time.time()
            response = requests.post('http://'+host+'/setpos?username='+username, data=json.dumps(fake_pos), headers={"Content-Type": "application/json"})
            latency = (time.time()-start)*100
            last_write = time.time()
        
        pygame.draw.rect(window, this_player['color'], (*fake_pos, cube_size, cube_size))
        for i in world['players']:
            if not i==username:
                if world['players'][i]['logged'][0] is True:pygame.draw.rect(window, world['players'][i]['color'], (*world['players'][i]['pos'], cube_size, cube_size))
        mean_latency = mean(latencies)
        write_interval = (mean_latency+write_margin)/100
        read_interval = (mean_latency+read_margin)/100
        print(f"Average latency: {str(int(mean_latency))}")
        print(f"Using interval: {str(interval)}")
        pygame.display.update()

        pygame.time.Clock().tick(60)
    except:
        pass

logoff()
pygame.quit()
sys.exit()