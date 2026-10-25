#!/usr/bin/env python3
"""Switch app icons to the active holiday set (America/Chicago). Restores MAIN otherwise."""
import datetime as dt,os,re,shutil,sys
from zoneinfo import ZoneInfo
def easter(y):
 a=y%19;b=y//100;c=y%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3;h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7;m=(a+11*h+22*l)//451;mo=(h+l-7*m+114)//31;da=(h+l-7*m+114)%31+1
 return dt.date(y,mo,da)
def nth_wd(y,mo,wd,n):
 d=dt.date(y,mo,1);d+=dt.timedelta((wd-d.weekday())%7);return d+dt.timedelta(7*(n-1))
def active(t):
 y=t.year;D=dt.date
 e=easter(y);md=nth_wd(y,5,6,2);tg=nth_wd(y,11,3,4)
 W=[('birthday',D(y,10,13),D(y,10,15)),('newyear',D(y,12,31),D(y,12,31)),('newyear',D(y,1,1),D(y,1,2)),('valentine',D(y,2,10),D(y,2,14)),('stpatricks',D(y,3,15),D(y,3,17)),
    ('easter',e-dt.timedelta(7),e+dt.timedelta(1)),('mothers',md-dt.timedelta(6),md),('july4',D(y,7,1),D(y,7,4)),('thanksgiving',tg-dt.timedelta(3),tg+dt.timedelta(3)),
    ('fall',D(y,10,20),D(y,10,31)),('christmas',D(y,12,15),D(y,12,26))]
 for n,a,b in W:
  if a<=t<=b:return n
 return 'main'
t=dt.datetime.now(ZoneInfo('America/Chicago')).date()
if len(sys.argv)>1:t=dt.date.fromisoformat(sys.argv[1])
s=active(t);src=f'icons/holiday/{s}'
print('date',t,'set',s)
ch=False
for f in os.listdir(src):
 a,b=f'{src}/{f}',f'icons/{f}'
 if not os.path.exists(b) or open(a,'rb').read()!=open(b,'rb').read():shutil.copyfile(a,b);ch=True
if ch:
 w=open('sw.js').read()
 w=re.sub(r'\n// holiday-icons: .*','',w).rstrip('\n')+f'\n// holiday-icons: {s} {t}\n'
 open('sw.js','w').write(w)
print('changed' if ch else 'unchanged')
