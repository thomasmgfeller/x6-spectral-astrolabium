#!/usr/bin/env python3
"""X6 Photonik · local acquisition service. Python >= 3.11, Linux."""
import argparse
import base64
import copy
import fcntl
import hashlib
import hmac
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import secrets
import shutil
import ssl
import signal
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from drivers import BASE, SCHEDULE_SHA, capture_tags, digest, save, shutter, snapshots, utc

LIVE = {"ARMED","RUNNING","STOPPING","ABORTING","SEALING"}
RID = re.compile(r"[0-9a-f]{32}\Z")
FILENAME = re.compile(r"[A-Za-z0-9_.-]{1,90}\Z")
RESERVE = 64*1024**2
class Conflict(ValueError): pass
class Cancelled(Exception): pass

def integer(x, a, b):
    return type(x) is int and a <= x <= b

def number(x,a,b):
    return type(x) in (int,float) and math.isfinite(x) and a<=x<=b

def device(d):
    return isinstance(d,dict) and isinstance(d.get("port"),str) and d["port"].startswith("/dev/") and re.fullmatch(r"[0-9]{8}",str(d.get("serial",""))) and isinstance(d["serial"],str)

def profile_check(p):
    if not isinstance(p,dict) or p.get("source") not in ("example","sagnac","swabian"):
        raise ValueError("Quelle muss example, sagnac oder swabian sein")
    if p["source"]=="sagnac" and (not str(p.get("port","")).startswith("/dev/") or p.get("baud") not in (115200,921600,1000000)):
        raise ValueError("Expliziter UART-Pfad und Baudrate erforderlich")
    if p["source"]=="swabian":
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}",str(p.get("serial",""))) or not isinstance(p.get("serial"),str):
            raise ValueError("Time-Tagger-Seriennummer fehlt")
        v=p.get("trigger_v")
        if not isinstance(v,list) or len(v)!=4 or not all(number(n,-2.5,2.5) for n in v):
            raise ValueError("Vier kalibrierte Triggerschwellen erforderlich")
    axes=p.get("axes")
    if axes is not None:
        if p["source"]!="swabian" or not isinstance(axes,list) or len(axes)!=2 or not all(device(a) for a in axes):
            raise ValueError("Zwei identifizierte ELL14 erforderlich")
        if len({a["serial"] for a in axes})!=2 or len({(a["port"],a.get("address")) for a in axes})!=2:
            raise ValueError("Doppelte Achse")
        for a in axes:
            if not re.fullmatch("[0-9A-F]",str(a.get("address",""))) or not number(a.get("zero_deg"),-360,360) or not integer(a.get("direction"),-1,1) or not a["direction"] or not number(a.get("tolerance_deg"),0.001,0.5):
                raise ValueError("Achsenparameter ungültig")
    if "shutter" in p and (not device(p["shutter"]) or p["source"]=="example"):
        raise ValueError("KSC101-Geräteidentität fehlt oder Beispielprofil")
    return p

def validate_config(p,c):
    if not isinstance(c,dict) or not isinstance(c.get("operator"),str) or not 1<=len(c["operator"].strip())<=80:
        raise ValueError("Verantwortliche Person angeben")
    if not isinstance(c.get("label"),str) or not 1<=len(c["label"].strip())<=80:
        raise ValueError("Laufbezeichnung fehlt")
    c={k:c[k].strip() for k in ("operator","label")} | {k:c.get(k) for k in ("mode","seconds","frames","first_sequence","timeout_s","calibration_sha256","local_ready")}
    if c["local_ready"] is not True:
        raise ValueError("Lokale Vorbereitung bestätigen")
    if p["source"]!="example" and not isinstance(c["calibration_sha256"],str):
        raise ValueError("Kalibrierdatei wählen")
    if p["source"]!="example" and not re.fullmatch("[0-9a-f]{64}",c["calibration_sha256"]):
        raise ValueError("Kalibrierhash ungültig")
    if p["source"]=="swabian":
        if c["mode"] not in ("fixed","schedule") or not integer(c["seconds"],1,3600):
            raise ValueError("Segmentparameter ungültig")
        if c["mode"]=="schedule" and not p.get("axes"):
            raise ValueError("80-Segment-Plan benötigt zwei konfigurierte Achsen")
    else:
        s=c["first_sequence"]
        if not isinstance(s,str) or not re.fullmatch(r"[0-9]{1,20}",s) or not integer(c["frames"],1,4096) or int(s)+c["frames"]>2**64 or not integer(c["timeout_s"],1,3600):
            raise ValueError("Framezahl, Sequenznummer oder Frist ungültig")
        if p["source"]=="example" and (s!="100" or c["frames"]!=4):
            raise ValueError("Beispiel benötigt vier Frames ab Sequenz 100")
    return c

class Bench:
    def __init__(self,root,profile):
        self.profile=profile_check(profile)
        self.root=Path(root).resolve()
        self.root.mkdir(mode=0o700,parents=True,exist_ok=True)
        self.lease=(self.root/".lock").open("a+")
        try:
            fcntl.flock(self.lease,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError:
            self.lease.close()
            raise
        self.lock=threading.RLock()
        self.state={"run_id":None,"state":"IDLE","phase":"IDLE"}
        self.thread=None
        self.cancel=threading.Event()
        self.shutter_sample=None
        self.cache={}
        for d in self.root.iterdir():
            if d.is_dir() and RID.fullmatch(d.name) and not (d/"manifest.json").exists():
                unfinished=d/"manifest.json.tmp"
                if unfinished.exists():
                    unfinished.rename(d/("unfinished-manifest-"+uuid.uuid4().hex+".json"))
                self.seal(d,{"state":"INTERRUPTED","run_id":d.name,"phase":"RECOVERY","reason":"Dienst ohne Abschluss beendet"})

    def seal(self,d,state):
        entries={}
        for path in sorted(d.iterdir()):
            if path.is_file() and not path.is_symlink() and path.name!="manifest.json":
                with path.open("rb") as data_file:
                    os.fsync(data_file.fileno())
                entries[path.name]={"bytes":path.stat().st_size,"sha256":digest(path)}
        save(d/"manifest.json", dict(schema="x6.photonics.run.v1", final=state, files=entries,
            finished_utc=utc(), physical_qualification="NOT_RUN",qed="NOT_APPLICABLE"))

    def journal(self,event,**fields):
        with (self.folder/"journal.jsonl").open("a",encoding="utf8") as f:
            f.write(json.dumps(dict(utc=utc(),event=event,**fields),ensure_ascii=False)+"\n")
            f.flush()
            os.fsync(f.fileno())

    def report(self,**fields):
        with self.lock:
            self.state.update(fields)
            self.state["updated_utc"]=utc()

    def status(self):
        with self.lock:
            return dict(api="x6.bench.v1", utc=utc(),source=self.profile["source"],axes=bool(self.profile.get("axes")),
                        shutter_configured="shutter" in self.profile,shutter=self.shutter_sample,
                        free_bytes=shutil.disk_usage(self.root).free,run=copy.deepcopy(self.state))
    def check(self):
        if self.cancel.is_set():
            raise Cancelled()
        if shutil.disk_usage(self.root).free < RESERVE:
            raise OSError("Speicherreserve unterschritten")

    def command(self,req):
        with self.lock:
            cmd=req.get("action")
            key=req.get("request_id")
            if not isinstance(key,str) or not RID.fullmatch(key):
                raise ValueError("Anforderungs-ID ungültig")
            sign=hashlib.sha256(json.dumps(req,sort_keys=True).encode()).hexdigest()
            if key in self.cache:
                if self.cache[key][0]!=sign:
                    raise Conflict("Befehls-ID mit verändertem Inhalt")
                return self.cache[key][1]
            if "run_id" not in req or req["run_id"]!=self.state["run_id"]:
                raise Conflict("Laufkontext veraltet")
            st=self.state["state"]
            if cmd=="arm":
                if st in LIVE or (self.thread and self.thread.is_alive()):
                    raise Conflict("Ein Lauf ist aktiv")
                cfg=validate_config(self.profile,req.get("config"))
                calibration=None
                if self.profile["source"]!="example":
                    encoded=req.get("calibration_b64")
                    if not isinstance(encoded,str) or not 1<=len(encoded)<=2_800_000:
                        raise ValueError("Kalibrierdatei fehlt oder zu groß")
                    calibration=base64.b64decode(encoded,validate=True)
                    if len(calibration)>2*1024**2 or hashlib.sha256(calibration).hexdigest()!=cfg["calibration_sha256"]:
                        raise ValueError("Kalibrierdatei stimmt nicht mit SHA-256 überein")
                self.cancel.clear()
                self.check()
                rid=uuid.uuid4().hex
                self.folder=self.root/rid
                self.folder.mkdir(mode=0o700)
                if calibration is not None:
                    (self.folder/"calibration.original").write_bytes(calibration)
                self.config=cfg
                profile=copy.deepcopy(self.profile)
                frozen=dict(run_id=rid,config=cfg,profile=profile,created_utc=utc(),version="0.1",source_revision="69db6c69dc580b6d2889d5ee5c5aa4d90034e85f")
                frozen["software_sha256"]={name:digest(BASE/name) for name in ("labor_server.py","drivers.py","vendor/analyze.py","vendor/frame_codec.py","X6_Photonik_Laborbuch.html")}
                if cfg["mode"]=="schedule" and profile["source"]=="swabian":
                    shutil.copyfile(BASE/"examples/schedule.csv",self.folder/"schedule.csv")
                    if digest(self.folder/"schedule.csv")!=SCHEDULE_SHA:
                        raise ValueError("Messplan verändert")
                save(self.folder/"config.json",frozen)
                self.state=dict(run_id=rid,state="ARMED",phase="CONFIG_FROZEN",source_open=False,frames=0,
                                bytes_received=0,events=None,flags=None,last_sequence=None,overflows=None,
                                origin="synthetic" if profile["source"]=="example" else "hardware_port",
                                config_sha256=digest(self.folder/"config.json"),started_utc=None)
                self.journal("arm",request_id=key)
            elif cmd=="start" and st=="ARMED":
                if self.state["config_sha256"]!=digest(self.folder/"config.json"):
                    raise Conflict("Konfiguration nach Freigabe verändert")
                if self.profile["source"]!="example" and digest(self.folder/"calibration.original")!=self.config["calibration_sha256"]:
                    raise Conflict("Archivierte Kalibrierdatei nach Freigabe verändert")
                self.journal("start",request_id=key)
                self.report(state="RUNNING",phase="OPENING",started_utc=utc())
                self.thread=threading.Thread(target=self.worker)
                self.thread.start()
            elif cmd in ("stop","abort") and st in ("ARMED","RUNNING"):
                self.journal(cmd,request_id=key)
                self.report(state="ABORTING" if cmd=="abort" else "STOPPING")
                self.cancel.set()
                if st=="ARMED":
                    self.finish("ABORTED" if cmd=="abort" else "STOPPED","Vor Erfassung beendet")
            elif cmd in ("shutter","shutter_off") and "shutter" in self.profile and st not in LIVE:
                self.shutter_sample=None
                station=self.root/"station.jsonl"
                def record(stage,**fields):
                    with station.open("a",encoding="utf8") as f:
                        f.write(json.dumps(dict(utc=utc(),action=cmd,stage=stage,request_id=key,**fields))+"\n")
                        f.flush()
                        os.fsync(f.fileno())
                record("request")
                try:
                    self.shutter_sample=shutter(self.profile["shutter"],deactivate=cmd=="shutter_off")
                except (OSError,ValueError) as e:
                    record("unconfirmed",reason=str(e))
                    raise
                record("readback",sample=self.shutter_sample)
            else:
                raise Conflict("Befehl im aktuellen Zustand nicht zulässig")
            ack=dict(action=cmd,run_id=self.state["run_id"],state=self.state["state"],scope="controller_readback" if cmd in ("shutter","shutter_off") else "host",utc=utc())
            self.cache[key]=(sign,ack)
            if len(self.cache)>512:
                self.cache.pop(next(iter(self.cache)))
            return ack

    def finish(self,result,reason):
        with self.lock:
            if self.state["state"]=="ABORTING" and result!="ERROR": result="ABORTED"
            if self.state["state"]=="STOPPING" and result!="ERROR": result="STOPPED"
            self.report(state="SEALING",phase="SEALING",source_open=False)
            final=dict(self.state,state=result,phase="CLOSED",reason=reason,closed_utc=utc())
        try:
            self.journal("final",result=result,reason=reason)
            self.seal(self.folder,final)
        except OSError as e:
            final.update(state="ARCHIVE_ERROR",reason=str(e))
        with self.lock:
            self.state=final

    def worker(self):
        result,reason="COMPLETE","Geplanter Erfassungsumfang beendet"
        try:
            fn=capture_tags if self.profile["source"]=="swabian" else snapshots
            fn(self.profile,self.config,self.folder,self.check,self.report)
        except Cancelled:
            result,reason="STOPPED","Auf Anforderung beendet"
        except Exception as e:
            result,reason="ERROR",f"{type(e).__name__}: {e}"
        self.finish(result,reason)

    def close(self):
        with self.lock:
            if self.state["state"] in ("ARMED","RUNNING"):
                self.command(dict(action="abort",request_id=uuid.uuid4().hex,run_id=self.state["run_id"]))
        if self.thread:
            self.thread.join()
        self.lease.close()

class Handler(BaseHTTPRequestHandler):
    server_version="X6Bench/0.1"
    def log_message(self,*args): pass
    def respond(self,status,obj,headers=()):
        data=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(data)))
        for k,v in headers: self.send_header(k,v)
        self.end_headers()
        self.wfile.write(data)
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","DENY")
        super().end_headers()
    def guard(self,post=False):
        origin=self.server.origin
        if self.headers.get("Host")!=urlsplit(origin).netloc or self.headers.get("Origin",origin)!=origin:
            self.respond(403,{"error":"Fremder Ursprung"});return False
        if post and (self.headers.get("Origin")!=origin or self.headers.get_content_type()!="application/json"):
            self.respond(403,{"error":"Gleicher Ursprung und JSON erforderlich"});return False
        return True
    def authenticated(self):
        from http.cookies import SimpleCookie
        c=SimpleCookie(self.headers.get("Cookie",""))
        if "x6lab" in c and hmac.compare_digest(c["x6lab"].value.encode(),self.server.session.encode()):
            return True
        self.respond(401,{"error":"Zugangscode des lokalen Dienstes erforderlich"});return False
    def file(self,path,kind,download=False):
        with path.open("rb") as f:
            self.send_response(200)
            self.send_header("Content-Type",kind)
            self.send_header("Content-Length",str(os.fstat(f.fileno()).st_size))
            if download: self.send_header("Content-Disposition",f'attachment; filename="{path.name}"')
            self.end_headers()
            shutil.copyfileobj(f,self.wfile,1024*1024)
    def do_GET(self):
        if not self.guard(): return
        path=urlsplit(self.path).path
        if path in ("/","/X6_Photonik_Laborbuch.html"):
            page=(BASE/"X6_Photonik_Laborbuch.html").read_bytes().replace(b"</head>",b'<meta name="x6-daemon" content="x6.bench.v1"></head>',1)
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return
        if not self.authenticated(): return
        bench=self.server.bench
        if path=="/api/status": return self.respond(200,bench.status())
        if path=="/api/archive":
            runs=[]
            for d in sorted(bench.root.iterdir(),key=lambda x:x.stat().st_mtime,reverse=True):
                if not RID.fullmatch(d.name) or not (d/"manifest.json").is_file(): continue
                m=json.loads((d/"manifest.json").read_text())
                runs.append(dict(id=d.name,state=m["final"]["state"],utc=m["finished_utc"],files=["manifest.json",*m["files"]]))
                if len(runs)==50: break
            return self.respond(200,runs)
        parts=path.split("/")
        if len(parts)==5 and parts[1:3]==["api","files"] and RID.fullmatch(parts[3]) and FILENAME.fullmatch(parts[4]):
            d=bench.root/parts[3]; m=d/"manifest.json"
            if m.is_file() and (parts[4]=="manifest.json" or parts[4] in json.loads(m.read_text())["files"]):
                return self.file(d/parts[4],"application/octet-stream",True)
        self.respond(404,{"error":"Unbekannte Ressource"})
    def do_POST(self):
        if not self.guard(True): return
        try:
            n=int(self.headers.get("Content-Length",0))
            if not 1<=n<=2_850_000: raise ValueError("Ungültige Anforderungslänge")
            x=json.loads(self.rfile.read(n))
            if not isinstance(x,dict): raise ValueError("JSON-Objekt erforderlich")
            if self.path=="/api/login":
                if not isinstance(x.get("token"),str) or not hmac.compare_digest(x["token"].encode(),self.server.token.encode()):
                    return self.respond(401,{"error":"Zugangscode ungültig"})
                cookie="x6lab="+self.server.session+"; HttpOnly; SameSite=Strict; Path=/api/"
                if self.server.origin.startswith("https:"): cookie+="; Secure"
                return self.respond(200,{"api":"x6.bench.v1"},[("Set-Cookie",cookie)])
            if not self.authenticated(): return
            if self.path=="/api/command": return self.respond(200,self.server.bench.command(x))
            self.respond(404,{"error":"Unbekannter Pfad"})
        except Conflict as e: self.respond(409,{"error":str(e)})
        except (ValueError,KeyError,TypeError) as e: self.respond(400,{"error":str(e)})
        except (OSError,RuntimeError) as e: self.respond(503,{"error":str(e)})
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profile",type=Path,help="JSON-Geräteprofil. Ohne Profil nur das synthetische Beispiel.")
    p.add_argument("--data",type=Path,default=Path("x6-runs"))
    p.add_argument("--bind",default="127.0.0.1",help="Numerische IPv4-Adresse")
    p.add_argument("--port",type=int,default=8765)
    p.add_argument("--cert",type=Path);p.add_argument("--key",type=Path)
    args=p.parse_args()
    addr=ipaddress.IPv4Address(args.bind)
    if addr.is_unspecified or bool(args.cert)!=bool(args.key) or (not addr.is_loopback and not args.cert):
        p.error("Explizite IP wählen. Für LAN sind Zertifikat und Schlüssel erforderlich.")
    os.umask(0o077)
    profile=json.loads(args.profile.read_text()) if args.profile else {"source":"example"}
    bench=Bench(args.data,profile)
    try:
        with ThreadingHTTPServer((str(addr),args.port),Handler) as srv:
            if args.cert:
                tls=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                tls.load_cert_chain(str(args.cert),str(args.key))
                srv.socket=tls.wrap_socket(srv.socket,server_side=True)
            srv.bench=bench
            srv.origin=("https" if args.cert else "http")+f"://{addr}:{srv.server_port}"
            srv.token=secrets.token_urlsafe(24)
            srv.session=secrets.token_urlsafe(32)
            print(f"Laborbuch: {srv.origin}/\nZugangscode: {srv.token}\nProfil: {profile['source']}",flush=True)
            def terminate(*_):
                raise KeyboardInterrupt()
            signal.signal(signal.SIGTERM,terminate)
            try: srv.serve_forever()
            except KeyboardInterrupt: pass
    finally:
        bench.close()
if __name__=="__main__":
    main()
